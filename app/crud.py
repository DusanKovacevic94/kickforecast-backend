from sqlalchemy.orm import Session
from . import models, schemas, auth

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Post CRUD
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_public_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).filter(models.Post.is_published == True).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_post_by_slug(db: Session, slug: str):
    return db.query(models.Post).filter(models.Post.slug == slug).first()

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post: schemas.PostUpdate):
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    
    update_data = post.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
