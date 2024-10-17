from datetime import datetime, timedelta, timezone
from os import walk
from dotenv import dotenv_values
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

env = dotenv_values(".env")

secret_key = env["SECRET_KEY"]
algorithm = env["ALGORITHM"]
token_expires = env["ACCESS_TOKEN_EXPIRE_MINUTES"]



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")



def create_jwt(data: dict, expires: timedelta=timedelta(minutes=15)):
    if(secret_key is None or algorithm is None or token_expires is None): 
        raise ValueError("Secret Key or Algorithm not set.")

    data_to_encode = data.copy()

    if (expires.total_seconds() > 0 ):
        expire = datetime.now(timezone.utc) + expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(token_expires))

    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, secret_key, algorithm)
    return encoded_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if(secret_key is None or algorithm is None or token_expires is None): raise ValueError("Secret Key or Algorithm not set.")

    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithm)
        email = payload.get("sub")
        if(email is None):
            raise credentials_exception
        return {"email": email}
    except JWTError as e:
        print(e)
        raise credentials_exception

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
