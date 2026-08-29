from pydantic import BaseModel,EmailStr
from datetime import datetime



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
            from_attributes = True


class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    pass
    id: int
    created_at: datetime


class UserCreate(BaseModel):
     email: EmailStr
     password: str

     class Config:
                 from_attributes = True

class UserResponse(BaseModel):
      email: EmailStr
      id: int
      created_at: datetime

class UserLogin(BaseModel):
      email: EmailStr
      password: str


