from fastapi import FastAPI, status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..database import engine,get_db
from .. import models,schemas,utils
from typing import List
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user: schemas.UserCreate,  db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password 
    
    new_user = models.User(**user.model_dump())

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"User with email {user.email} already exists.")

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)

def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} does not exists.")

    return user
