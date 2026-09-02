from pydantic import BaseModel,EmailStr,conint
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
    owner_id: int
    owner: UserResponse


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

class Token(BaseModel):
      access_token: str
      token_type: str

class TokenData(BaseModel):
      id: int | None = None

class Vote(BaseModel):
      post_id: int
      dir: conint(ge=0,le=1)

     
