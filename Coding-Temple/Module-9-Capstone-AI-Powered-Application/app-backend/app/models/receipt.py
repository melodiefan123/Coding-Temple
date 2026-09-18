import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    merchant_name = Column(String, index=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    category = Column(String, default="Uncategorized")
    transaction_date = Column(DateTime, nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())
    is_verified = Column(Boolean, default=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="receipts")
    chromadb_id = Column(String, unique=True, nullable=False)