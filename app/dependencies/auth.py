from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.models import User

from app.services.user_service import get_user_by_username
from app.services.auth_service import decode_access_token

from app.dependencies.db import get_db


from typing import Annotated

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token=token)
        user = get_user_by_username(db=db, username=payload["sub"])
    except:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user
