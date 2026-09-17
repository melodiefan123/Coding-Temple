from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_name = Column(String, nullable=False)       # e.g., "Chase Sapphire", "Business Amex"
    card_type = Column(String, nullable=False)       # e.g., "Visa", "Mastercard", "Amex"
    last_four = Column(String(4), nullable=False)    # e.g., "4321"
    credit_limit = Column(Float, default=0.0)
    current_balance = Column(Float, default=0.0)
    user = relationship("User", back_populates="cards")
    subscriptions = relationship(
        "Subscription", 
        back_populates="card", 
        cascade="all, delete-orphan"
    )
    