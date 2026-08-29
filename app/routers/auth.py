from fastapi import FastAPI, status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils

router = APIRouter(tags=["authentication"])


@router.post("/login")
def login(user_credentials:schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    # create token
    # return token

    return {"token": "example token"}

    










