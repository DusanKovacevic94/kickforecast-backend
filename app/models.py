from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    EDITOR = "editor"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.EDITOR)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    summary = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_published = Column(Boolean, default=False)
    
    # For football predictions specifically
    match_date = Column(DateTime(timezone=True), nullable=True)
    home_team = Column(String, nullable=True)
    away_team = Column(String, nullable=True)
    prediction = Column(String, nullable=True)
    odds = Column(String, nullable=True)
    hero_image = Column(String, nullable=True)
    og_image = Column(String, nullable=True)

    author = relationship("User", back_populates="posts")
