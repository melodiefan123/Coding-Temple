# project/starter/app/auth.py
# Module 5 Project — JWT and password utilities
#
# TODO: Implement password hashing and JWT functions

from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.database import get_db
from app.exceptions import AppException
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# TODO: Create pwd_context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def hash_password(password: str) -> str:
    """TODO: hash with pwd_context"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """TODO: verify with pwd_context"""
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    """TODO: create JWT with expiry"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """TODO: decode JWT and return current user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None: 
            raise AppException(detail="Invalid Token",status_code=401)
    except JWTError: 
        raise AppException(detail="Invalid or expired Token", status_code=401)
    from app.models.user import User
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None: 
        raise AppException( detail="User not found", status_code=401)
    return user

