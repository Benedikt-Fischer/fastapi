"""
Auth / Login routes
"""

from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
#TODO fix attempted relative import beyond top-level package
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
#def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          database: Session = Depends(get_db)):
    """Login user by email / password, verify user exists,
    verify password, generate and return access_token"""
    user = database.query(models.User).filter(
           models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}
