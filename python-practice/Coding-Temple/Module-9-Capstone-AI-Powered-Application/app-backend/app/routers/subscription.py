from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse
from app.auth import get_current_user
from app.models.user import User
from app.models.card import Card



router = APIRouter(prefix="/cards", tags=["Subscriptions"])

# Get all subscriptions for a specific card
@router.get("/{card_id}/subscriptions", response_model=List[SubscriptionResponse])
def get_card_subscriptions(
    card_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    card = db.query(Card).filter(
        Card.id == card_id, 
        Card.user_id == current_user.id
    ).first()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found or unauthorized")

    # 2. Fetch subscriptions linked to this card
    subscriptions = db.query(Subscription).filter(
        Subscription.card_id == card_id
    ).all()

    return subscriptions

# Add a subscription to a card
@router.post("/subscriptions")
async def create_subscription(payload: SubscriptionCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    card = db.query(Card).filter(Card.id == payload.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    new_subscription = Subscription(
        **payload.model_dump(),
        user_id=card.user_id,  # 👈 Pass user_id explicitly from the card
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

