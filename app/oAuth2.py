from jose import JWTError,jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import schemas,database,models
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings


oAuth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#SECRET_KEY
#ALGORITHM
#EXPIRE

SECRET_ACCESS_KEY = settings.secret_access_key
ALGORITHM = settings.algorithm
EXPIRE_ACCESS_TOKEN = settings.access_token_expire_minutes




def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=EXPIRE_ACCESS_TOKEN)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_ACCESS_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credential_exception):

    try:
        payload = jwt.decode(token,SECRET_ACCESS_KEY,algorithms=[ALGORITHM])

        id: int = payload.get("user_id")

        if not id:
            raise credential_exception

        token_data = schemas.TokenData(id=id)

        return token_data

    except JWTError:
        raise credential_exception



def get_current_user(token: str = Depends(oAuth2_scheme), db: Session = Depends(database.get_db)):


    credential_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credential",headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)
    current_user = db.query(models.User).filter(models.User.id == token.id).first() 
    
    return current_user


