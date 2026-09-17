from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime, timezone
from app.database import Base

class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source = Column(String, nullable=False)  # e.g., "Consulting", "Investments"
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
