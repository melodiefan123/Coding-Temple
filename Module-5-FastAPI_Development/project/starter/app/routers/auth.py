# project/starter/app/routers/auth.py
# Module 5 Project — Auth endpoints
#
# TODO: Implement POST /register, POST /token, GET /me

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.database import get_db

router = APIRouter()


# TODO: POST /register
@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    pass


# TODO: POST /token
@router.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    pass


# TODO: GET /me
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(None)):  # TODO: replace None
    pass
