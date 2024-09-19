from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from typing import Annotated

from app.schemas.user_schema import UserCreate, LoginRequest, UserRead

from app.services.user_service import (
    get_user_by_username,
    get_user_by_email,
    create_user,
)
from app.services.auth_service import generate_jwt, get_current_user


router = APIRouter()


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
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
    created_user = create_user(db, user)
    token = generate_jwt(created_user.username, created_user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado"
        )
    elif user.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta"
        )
    token = generate_jwt(user.username, user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def get_user_info(current_user: Annotated[UserRead, Depends(get_current_user)]):
    return current_user
