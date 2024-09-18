# services/user.py
import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user_schema import UserCreate

# Configuración para JWT
SECRET_KEY = "mysecretkey"  # Usa una clave secreta robusta en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_user(db: Session, user_create: UserCreate):
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        password=user_create.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def generate_jwt(username: str, email: str) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": username, "email": email, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
