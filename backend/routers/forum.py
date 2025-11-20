from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import User, Post, Comment, Like
from backend.schemas import PostCreate, PostResponse, CommentCreate, CommentResponse
from backend.dependencies import get_current_active_user

router = APIRouter(prefix="/forum", tags=["forum"])

@router.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    new_post = Post(
        title=post.title,
        content=post.content,
        user_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # Manually populate response with required fields
    # Pydantic v2 uses model_validate instead of from_orm
    response_data = {
        "id": new_post.id,
        "title": new_post.title,
        "content": new_post.content,
        "user_id": new_post.user_id,
        "created_at": new_post.created_at,
        "username": current_user.username,
        "comments": [],
        "likes_count": 0
    }
    return PostResponse(**response_data)

@router.get("/posts", response_model=List[PostResponse])
def get_posts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    results = []
    for post in posts:
        # Build comments list
        comments_list = []
        for comment in post.comments:
            comments_list.append({
                "id": comment.id,
                "content": comment.content,
                "user_id": comment.user_id,
                "created_at": comment.created_at,
                "username": comment.author.username
            })
        
        # Build response
        response_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "created_at": post.created_at,
            "username": post.author.username,
            "comments": comments_list,
            "likes_count": len(post.likes)
        }
        results.append(PostResponse(**response_data))
    return results

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(
    post_id: int, 
    comment: CommentCreate, 
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    new_comment = Comment(
        content=comment.content,
        post_id=post_id,
        user_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    # Build response with username
    response_data = {
        "id": new_comment.id,
        "content": new_comment.content,
        "user_id": new_comment.user_id,
        "created_at": new_comment.created_at,
        "username": current_user.username
    }
    return CommentResponse(**response_data)

@router.post("/posts/{post_id}/like")
def like_post(
    post_id: int, 
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    existing_like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == current_user.id).first()
    if existing_like:
        db.delete(existing_like)
        db.commit()
        return {"message": "Unliked"}
    else:
        new_like = Like(post_id=post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Liked"}

