import io
import re
import pandas as pd
import pypdf
from datetime import datetime
from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.security import get_current_user


from app.database import get_db
from app.models.income import Income
from app.models.expense import Expense
from app.models.statement import Statement
from app.schemas.statement import (
    StatementUploadResponse, 
    StatementSyncRequest, 
    StatementSyncResponse,
    StatementTransaction
)

router = APIRouter(prefix="/statements", tags=["Statements"])

# ------------------------------------------------------------------
# PARSER LOGIC (CSV & PDF)
# ------------------------------------------------------------------

def parse_csv_statement(file_bytes: bytes) -> List[StatementTransaction]:
    """Parses standard bank CSV files into income and expense records."""
    df = pd.read_csv(io.BytesIO(file_bytes))
    
    # Normalize column names to lowercase for robust matching
    cols_map = {str(col).strip().lower(): col for col in df.columns}
    
    # Identify key columns dynamically
    date_col = next((cols_map[c] for c in cols_map if "date" in c), None)
    desc_col = next((cols_map[c] for c in cols_map if any(k in c for k in ["desc", "name", "payee", "memo", "details"])), None)
    
    amount_col = next((cols_map[c] for c in cols_map if "amount" in c), None)
    debit_col = next((cols_map[c] for c in cols_map if any(k in c for k in ["debit", "withdrawal", "out"])), None)
    credit_col = next((cols_map[c] for c in cols_map if any(k in c for k in ["credit", "deposit", "in"])), None)
    category_col = next((cols_map[c] for c in cols_map if "cat" in c), None)

    transactions = []

    for _, row in df.iterrows():
        # Skip completely empty rows
        if row.isna().all():
            continue

        date_val = str(row[date_col]).strip() if date_col and pd.notna(row[date_col]) else datetime.now().strftime("%Y-%m-%d")
        desc_val = str(row[desc_col]).strip() if desc_col and pd.notna(row[desc_col]) else "Bank Transaction"
        cat_val = str(row[category_col]).strip() if category_col and pd.notna(row[category_col]) else "Uncategorized"

        amount = 0.0
        tx_type = "expense"

        # Case A: Separate Debit and Credit columns
        if debit_col or credit_col:
            debit_val = pd.to_numeric(row.get(debit_col), errors='coerce') if debit_col else None
            credit_val = pd.to_numeric(row.get(credit_col), errors='coerce') if credit_col else None

            if pd.notna(credit_val) and abs(float(credit_val)) > 0:
                amount = abs(float(credit_val))
                tx_type = "income"
            elif pd.notna(debit_val) and abs(float(debit_val)) > 0:
                amount = abs(float(debit_val))
                tx_type = "expense"
            else:
                continue

        # Case B: Single Amount column with +/- signs
        elif amount_col and pd.notna(row[amount_col]):
            raw_amt_str = str(row[amount_col]).replace("$", "").replace(",", "").strip()
            try:
                raw_amt = float(raw_amt_str)
                if raw_amt < 0:
                    amount = abs(raw_amt)
                    tx_type = "expense"
                else:
                    amount = raw_amt
                    tx_type = "income"
            except ValueError:
                continue
        else:
            continue

        transactions.append(
            StatementTransaction(
                date=date_val,
                description=desc_val,
                amount=round(amount, 2),
                transaction_type=tx_type,
                category=cat_val
            )
        )

    return transactions


def parse_pdf_statement(file_bytes: bytes) -> List[StatementTransaction]:
    """Parses text lines in PDF statements matching tabular transaction patterns."""
    pdf_reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    full_text = ""
    for page in pdf_reader.pages:
        txt = page.extract_text()
        if txt:
            full_text += txt + "\n"

    # Regex pattern matching: Date | Description | Amount ($1,234.56 or -$123.45)
    pattern = re.compile(
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\s+(.*?)\s+([+-]?\$?\s*-?\d[\d,]*\.\d{2})'
    )

    transactions = []
    for line in full_text.splitlines():
        match = pattern.search(line.strip())
        if match:
            date_str, desc_str, amt_str = match.groups()
            
            clean_amt_str = amt_str.replace("$", "").replace(",", "").replace(" ", "")
            try:
                raw_amt = float(clean_amt_str)
                if raw_amt < 0 or "-" in amt_str:
                    tx_type = "expense"
                    amount = abs(raw_amt)
                else:
                    tx_type = "income"
                    amount = raw_amt

                transactions.append(
                    StatementTransaction(
                        date=date_str,
                        description=desc_str.strip(),
                        amount=round(amount, 2),
                        transaction_type=tx_type,
                        category="Uncategorized"
                    )
                )
            except ValueError:
                continue

    return transactions


# ------------------------------------------------------------------
# ROUTE HANDLERS
# ------------------------------------------------------------------

@router.post("/upload", response_model=StatementUploadResponse)
async def upload_bank_statement(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = file.filename.lower()
    file_bytes = await file.read()

    if filename.endswith(".csv"):
        extracted_items = parse_csv_statement(file_bytes)
        file_type = "csv"
    elif filename.endswith(".pdf"):
        extracted_items = parse_pdf_statement(file_bytes)
        file_type = "pdf"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file extension. Only .csv and .pdf are supported."
        )

    if not extracted_items:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not extract any transaction rows. Check the file layout."
        )

    # Log file record in database
    stmt_record = Statement(
        filename=file.filename,
        file_type=file_type,
        processed=True
    )
    db.add(stmt_record)
    db.commit()

    return StatementUploadResponse(
        filename=file.filename,
        total_extracted=len(extracted_items),
        transactions=extracted_items,
        message=f"Parsed {len(extracted_items)} transactions successfully."
    )


@router.post("/confirm", response_model=StatementSyncResponse)
async def confirm_and_sync(
    payload: StatementSyncRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)

):
    income_count = 0
    expense_count = 0

    for item in payload.transactions:
        parsed_date = datetime.strptime(item.date, "%Y-%m-%d").date() if isinstance(item.date, str) else item.date
        if item.transaction_type == "expense":
            db.add(Expense(
                description=item.description,
                amount=float(item.amount),
                category=item.category or "General",
                date=parsed_date,
                user_id=current_user.id
            ))
            expense_count += 1
        elif item.transaction_type == "income":
            db.add(Income(
                source=item.description,
                amount=float(item.amount),
                category=item.category or "Income",
                date=parsed_date,
                user_id=current_user.id
            ))
            income_count += 1

    db.commit()

    return StatementSyncResponse(
        income_records_added=income_count,
        expense_records_added=expense_count,
        message=f"Successfully synced {income_count + expense_count} transactions to your ledger."
    )