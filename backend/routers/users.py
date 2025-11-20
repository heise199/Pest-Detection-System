from fastapi import APIRouter, Depends
from backend.models import User
from backend.schemas import UserResponse
from backend.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

