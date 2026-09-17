# project/starter/app/routers/auth.py
# Module 5 Project — Auth endpoints
#
# TODO: Implement POST /register, POST /token, GET /me
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.database import get_db
from app.exceptions import AppException, DuplicateException,ForbiddenException, NotFoundException

router = APIRouter()


# TODO: POST /register
@router.post("/register", response_model=TokenResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user"""
    existing = db.query(User).filter(User.email == user.email).first()
    if existing: 
        raise DuplicateException("User", "email", user.email)
    user = User(
        name = user.username, 
        email = user.email,
        hashed_password = hash_password(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
    



# TODO: POST /token
@router.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Allows login if user exists"""
    user = db.query(User).filter(
    or_(User.email == form_data.username, User.name == form_data.username)
    ).first()    
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise AppException(detail="Invalid email or password",status_code=401)
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}



