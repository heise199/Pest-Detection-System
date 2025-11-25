from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# PestInfo Schemas
class PestInfoBase(BaseModel):
    name: str
    description: Optional[str] = None
    control_methods: Optional[str] = None
    image_url: Optional[str] = None

class PestInfoCreate(PestInfoBase):
    pass

class PestInfoResponse(PestInfoBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Detection Schemas
class DetectionCreate(BaseModel):
    pass

class DetectionResponse(BaseModel):
    id: int
    image_path: Optional[str]
    video_path: Optional[str]
    result_json: Optional[Dict[str, Any]]
    detection_type: str
    created_at: datetime

    class Config:
        from_attributes = True

# Forum Schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    username: str  # Enriched field

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: datetime
    comments: List[CommentResponse] = []
    likes_count: int
    username: str # Enriched field

    class Config:
        from_attributes = True

