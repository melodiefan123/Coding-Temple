from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base  # Adjust import based on your project structure

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 👈 Add this
    name = Column(String, nullable=False)              # e.g., "Netflix", "Spotify"
    amount = Column(Float, nullable=False)             # e.g., 15.99
    billing_cycle = Column(String, default="monthly")  # e.g., "monthly", "yearly"
    next_billing_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Optional relationship back to Card
    card = relationship("Card", back_populates="subscriptions")