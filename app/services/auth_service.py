from typing import Annotated, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone

from app.models import User

from app.schemas.user_schema import UserRead

from app.db import get_db

# Configura los parámetros de JWT
SECRET_KEY = "mysecretkey"  # Usa una clave secreta robusta en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependencia para obtener el token de la cabecera de autorización
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def generate_jwt(username: str, email: str) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": username, "email": email, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    print("TOKEN", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Aquí puedes realizar más validaciones si es necesario
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserRead:
    decoded_token = verify_token(token)
    user = db.query(User).filter(User.username == decoded_token["sub"]).first()
    return UserRead(id=user.id, username=user.username, email=user.email)
