# project/starter/app/auth.py
# Module 5 Project — JWT and password utilities
#
# TODO: Implement password hashing and JWT functions

from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import get_db
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# TODO: Create pwd_context with bcrypt
pwd_context = None  # TODO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def hash_password(password: str) -> str:
    """TODO: hash with pwd_context"""
    pass


def verify_password(plain: str, hashed: str) -> bool:
    """TODO: verify with pwd_context"""
    pass


def create_access_token(data: dict) -> str:
    """TODO: create JWT with expiry"""
    pass


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """TODO: decode JWT and return current user"""
    pass
