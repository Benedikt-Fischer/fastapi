"""
User routes
"""

from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
#TODO fix attempted relative import beyond top-level package
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, database: Session = Depends(get_db)):
    """Create user by schema"""
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(user_id: int, database: Session = Depends(get_db)):
    """Get user info from database by id"""
    user = database.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {user_id} does not exist")
    return user
