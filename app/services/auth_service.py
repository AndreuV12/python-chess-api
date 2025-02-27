from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
import jwt
from app.services.user_service import get_user_by_username

SECRET_KEY = "mysecretkey"  # Usa una clave secreta robusta en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def get_authenticated_user(db: Session, username: str, password: str):
    user = get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    elif password != user.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
