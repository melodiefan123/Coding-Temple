from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.card import Card
from app.auth import get_current_user
from app.schemas.card import CardCreate, CardResponse

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def add_card(
    card_in: CardCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_card = Card(
        user_id=current_user.id,
        **card_in.model_dump()
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@router.get("/", response_model=List[CardResponse])
def get_user_cards(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Card).filter(Card.user_id == current_user.id).all()
