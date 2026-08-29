
from jose import JWTError,jwt
from datetime import datetime, timedelta


#SECRET_KEY
#ALGORITHM
#EXPIRE

SECRET_ACCESS_KEY = "o9aLLhHKKfsFL451sliJHGafFla25fchUSD551aetFVSZR2sHF"
ALGORITHM = "HS256"
EXPIRE_ACCESS_TOKEN = 30



def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=EXPIRE_ACCESS_TOKEN)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_ACCESS_KEY, algorithm=ALGORITHM)

    return encoded_jwt
    


    