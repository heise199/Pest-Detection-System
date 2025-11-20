from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import User, PestInfo
from backend.schemas import PestInfoCreate, PestInfoResponse, UserResponse
from backend.dependencies import get_current_admin_user, get_current_active_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/pests", response_model=PestInfoResponse)
def create_pest_info(
    pest: PestInfoCreate, 
    current_user: User = Depends(get_current_admin_user), 
    db: Session = Depends(get_db)
):
    db_pest = PestInfo(**pest.dict())
    db.add(db_pest)
    db.commit()
    db.refresh(db_pest)
    return db_pest

@router.get("/pests", response_model=List[PestInfoResponse])
def get_pests(db: Session = Depends(get_db)):
    return db.query(PestInfo).all()

from sqlalchemy import func
from backend.models import User, PestInfo, Detection

@router.get("/stats")
def get_stats(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()
    total_detections = db.query(Detection).count()
    
    # Group by pest type (This is a simplification, assuming result_json holds the main class or we parse it)
    # Ideally we query the JSON, but MySQL JSON querying can be complex. 
    # For this demo, we just return raw counts or mock data if JSON parsing is too complex for simple SQL.
    # A better approach for production: normalize detection results into a separate table.
    
    # Simple approach: return total counts.
    
    return {
        "total_users": total_users,
        "total_detections": total_detections,
    }

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    return db.query(User).all()

