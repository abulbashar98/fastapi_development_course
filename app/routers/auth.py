from fastapi import FastAPI, status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils,oAuth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["authentication"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    # create token
    # return token

    access_token = oAuth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

    










