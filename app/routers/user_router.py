from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from typing import Annotated

from app.schemas.user_schema import UserCreate, UserRead

from app.services.auth_service import create_access_token

from app.services.user_service import (
    get_user_by_username,
    get_user_by_email,
    create_user,
)

router = APIRouter()


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user_with_username = get_user_by_username(db, user.username)
    if existing_user_with_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso.",
        )
    existing_user_with_email = get_user_by_email(db, user.email)
    if existing_user_with_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está en uso.",
        )
    created_user = create_user(db, user)
    acces_token_data = {"sub": created_user.username, "email": created_user.email}
    token = create_access_token(data=acces_token_data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = get_user_by_username(db=db, username=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario no encontrado"
        )
    elif form_data.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    acces_token_data = {"sub": user.username, "email": user.email}
    token = create_access_token(data=acces_token_data)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def get_user_info(current_user: Annotated[UserRead, Depends(get_current_user)]):
    return current_user
