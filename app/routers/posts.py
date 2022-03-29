"""
Posts Routes
Need to be logged in for all of these
"""
#TODO fix unused argument 'current_user?

from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
#TODO fix attempted relative import beyond top-level package
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(database: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    """Get all posts, require database, can set several params
    return all posts"""
    #all_posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #all_posts = (db.query(models.Post).filter(models.Post.title.contains(search))
    #            .limit(limit).offset(offset).all())
    #return all_posts

    all_posts = (database.query(models.Post, func.count(models.Vote.post_id).label("votes"))
                .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
                .group_by(models.Post.id).filter(models.Post.title.contains(search))
                .limit(limit).offset(offset).all())
    return all_posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, database: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    """Create post, require the post data, database, current user
    return the new post"""
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    database.add(new_post)
    database.commit()
    database.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(post_id: int, database: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    """Get one post by id, require post id, database, return the post"""
    #single_post = db.query(models.Post).filter(models.Post.id == id).first()
    single_post = (database.query(models.Post, func.count(models.Vote.post_id).label("votes"))
                  .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
                  .group_by(models.Post.id).filter(models.Post.id == post_id).first())
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")
    ## if only get posts that belong to user
    #if single_post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                        detail="Not authorized to perform this action!")
    return single_post

@router.delete("/{id}")
def delete_post(post_id: int, database: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    """Delete post by id, can only be done by owner of post
    require post id, database, current user, return only 204 code"""
    post_query = database.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not autorized to perform this action!")
    post_query.delete(synchronize_session=False)
    database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(post_id: int, updated_post: schemas.PostCreate, database: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    """Update post by id, can only be modified by the owner of the post
    require post id, updated post as schema, database and current user
    return the updated post as schema"""
    post_query = database.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action!")
    post_query.update(updated_post.dict(), synchronize_session=False)
    database.commit()
    return post_query.first()
