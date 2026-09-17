from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.database import get_db
from app.exceptions import AppException
import os
from app.models.user import User
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# TODO: Create pwd_context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def hash_password(password: str) -> str:
    """TODO: hash with pwd_context"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """TODO: verify with pwd_context"""
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    # Use timezone-aware UTC datetime
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # <--- Make sure this is enough time
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    print(f"--- ENCODING TOKEN WITH SECRET KEY: '{SECRET_KEY}' ---")
    print(f"--- GENERATED TOKEN: '{encoded_jwt}' ---")
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """TODO: decode JWT and return current user"""
    cleaned_token = token.strip()

    print(f"--- DECODING TOKEN WITH SECRET KEY: '{SECRET_KEY}' ---")
    print(f"--- RECEIVED TOKEN TO DECODE: '{cleaned_token}' ---")
    try:
        payload = jwt.decode(cleaned_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None: 
            raise AppException(detail="Invalid Token",status_code=401)
        user_id = int(user_id)
    except JWTError as e: 
        print(f"--- JWT DECODE FAILURE REASON: {e} ---") # <--- THIS WILL PRINT THE EXACT CAUSE
        raise AppException(status_code=401, detail="Invalid or expired Token")
   
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None: 
        raise AppException( detail="User not found", status_code=401)
    return user

