from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# from app.db import get_db
from sqlalchemy.orm import Session
from app.models import User

from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "mysecretkey"  # Cambia esto por una clave secreta fuerte
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.name == username).first()
    return user and password == user.password


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar el token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Buscar al usuario en la base de datos
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# authenticate_user("Andreu", "Andreu0521!",  )
