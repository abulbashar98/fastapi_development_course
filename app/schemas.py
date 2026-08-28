from pydantic import BaseModel,EmailStr
from datetime import datetime



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
            orm_mode = True


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
                 orm_mode = True

class UserResponse(BaseModel):
      email: EmailStr
      id: int
      created_at: datetime


