from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/invoices", tags=["Invoices"])

def ensure_datetime(dt):
    """Converts plain date objects into datetime objects for SQLAlchemy DateTime columns."""
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return datetime.combine(dt, datetime.min.time())
    return dt

@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(
    invoice: InvoiceCreate, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    # Unpack schema dict
    invoice_data = invoice.model_dump()

    # 1. Convert Enum to string value for DB string column
    if hasattr(invoice.status, "value"):
        invoice_data["status"] = invoice.status.value

    # 2. Ensure date/datetime compatibility
    invoice_data["issued_date"] = ensure_datetime(invoice.issued_date)
    invoice_data["due_date"] = ensure_datetime(invoice.due_date)

    # 3. Instantiate model cleanly
    new_invoice = Invoice(
        **invoice_data,
        user_id=current_user.id
    )
    
    try:
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)
        return new_invoice
    except Exception as e:
        db.rollback()
        print(f"Database insertion failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create invoice: {str(e)}"
        )

@router.get("/", response_model=list[InvoiceResponse])
def get_invoices(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    invoices = db.query(Invoice).filter(Invoice.user_id == current_user.id).all()
    return invoices

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == current_user.id).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice