"""
Define schemas for the http operations
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class UserCreate(BaseModel):
    """Schema required when creating a user"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema returned when creating user and getting user by id"""
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        """Tells pydantic to allow orm models"""
        orm_mode = True

class PostBase(BaseModel):
    """Schema serving as base for other Post schemas"""
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

class PostCreate(PostBase):
    """Schema required when creating and updating posts"""
    pass

#class PostUpdate(PostBase):
#    published: bool

class PostResponse(PostBase):
    """Schema returned when creating and updating posts"""
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        """Tells pydantic to allow orm models"""
        orm_mode = True

class PostVoteResponse(BaseModel):
    """Schema returned when getting all posts or one post by id"""
    Post: PostResponse
    votes: int

#class UserLogin(BaseModel):
#    email: EmailStr
#    password: str

class Token(BaseModel):
    """Schema returned when logging in / creating token"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema returned when verifying_access_token in oauth2"""
    id: Optional[str]

class Vote(BaseModel):
    """Schema for votes"""
    post_id: int
    dir: conint(ge=0, le=1)
