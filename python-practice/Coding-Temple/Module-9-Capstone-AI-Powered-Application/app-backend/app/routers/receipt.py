import shutil 
import uuid 
from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate, ReceiptResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/receipts", tags=["Receipts"])

UPLOAD_DIR = Path("uploads/receipts")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the upload directory exists

@router.post("/upload", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
def upload_receipt(
    merchant_name: str = Form(...),
    total_amount: float = Form(...),
    category: str = Form("Uncategorized"),
    transaction_date: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_receipt = Receipt(
        merchant_name=merchant_name,
        total_amount=total_amount,
        category=category,
        transaction_date=transaction_date,
        image_url = str(file_path),
        user_id=current_user.id,
    )
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)
    return new_receipt

@router.post("/", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_receipt(receipt: ReceiptCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_receipt = Receipt(
        **receipt.model_dump(),
        user_id=current_user.id
    )
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)
    return new_receipt

@router.get("/", response_model=list[ReceiptResponse])
def get_receipts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    receipts = db.query(Receipt).filter(Receipt.user_id == current_user.id).all()
    return receipts

@router.get("/{receipt_id}", response_model=ReceiptResponse)
def get_receipt(receipt_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id, Receipt.user_id == current_user.id).first()
    if not receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    return receipt  