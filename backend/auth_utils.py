from jose import jwt,JWTError
from fastapi import HTTPException,status
from config import SECRET_KEY, ALGORITHM

def verify_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid or expired token'
        )
