from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserResponse
from app.auth import get_current_user

router = APIRouter()
# TODO: GET /me
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):  # TODO: replace None
    """Returns the current user"""
    return current_user