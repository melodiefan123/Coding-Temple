from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base  # Import your SQLAlchemy Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False, default="Expense Entry")
    category = Column(String, nullable=False, index=True, default="General")
    amount = Column(Float, nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=True) # Set nullable=False if card is required
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=True) # or DateTime

    # Optional SQLAlchemy relationship if you have a Card model defined:
    # card = relationship("Card", back_populates="expenses")