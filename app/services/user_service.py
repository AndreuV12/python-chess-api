from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user_schema import UserCreate


def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


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


def register_user(db: Session, user: UserCreate):
    existing_user_with_username = get_user_by_username(db, user.username)
    if existing_user_with_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso.",
        )

    existing_user_with_email = get_user_by_email(db, user.email)
    if existing_user_with_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está en uso.",
        )
    return create_user(db, user)
