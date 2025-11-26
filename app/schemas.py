from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import UserRole

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.EDITOR
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

# Post Schemas
class PostBase(BaseModel):
    title: str
    slug: str
    content: str
    summary: Optional[str] = None
    is_published: bool = False
    match_date: Optional[datetime] = None
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    prediction: Optional[str] = None
    odds: Optional[str] = None
    hero_image: Optional[str] = None
    og_image: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: User

    class Config:
        orm_mode = True
