from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas, database, auth

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

# Public endpoints
@router.get("/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_public_posts(db, skip=skip, limit=limit)

@router.get("/{slug}", response_model=schemas.Post)
def read_post(slug: str, db: Session = Depends(database.get_db)):
    db_post = crud.get_post_by_slug(db, slug=slug)
    if db_post is None or not db_post.is_published:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# Protected endpoints (CMS)
@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    return crud.create_post(db=db, post=post, user_id=current_user.id)

@router.get("/cms/all", response_model=List[schemas.Post])
def read_all_posts_cms(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    return crud.get_posts(db, skip=skip, limit=limit)

@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    # Only admin or author can edit
    if current_user.role != models.UserRole.ADMIN and db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    return crud.update_post(db=db, post_id=post_id, post=post)

@router.delete("/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    # Only admin or author can delete
    if current_user.role != models.UserRole.ADMIN and db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    return crud.delete_post(db=db, post_id=post_id)
