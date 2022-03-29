"""
Vote routes
Need to be logged in for all of these
"""

from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
#TODO fix unused argument 'current_user?
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def do_vote(vote: schemas.Vote, database: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    """Add or substract vote on post
    One user can only add / substract vote on one post once
    require vote as schema, database current user
    return code / message if successfull or not"""
    post = database.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {vote.post_id} does not exist")

    vote_query = (database.query(models.Vote).filter(models.Vote
                 .post_id == vote.post_id, models.Vote.user_id == current_user.id))
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                  detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        database.add(new_vote)
        database.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        database.commit()
        return {"message": "Successfully deleted vote"}
