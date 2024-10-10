from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from typing import Annotated

from app.schemas.user_schema import UserCreate, UserRead

from app.services.user_service import register_user
from app.services.auth_service import get_authenticated_user, create_access_token

router = APIRouter()


@router.post("/register")
async def register_user_route(user: UserCreate, db: Session = Depends(get_db)):
    created_user = register_user(db, user)
    access_token_data = {"sub": created_user.username, "email": created_user.email}
    token = create_access_token(data=access_token_data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(
        db=db, username=form_data.username, password=form_data.password
    )
    access_token_data = {"sub": user.username, "email": user.email}
    token = create_access_token(data=access_token_data)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def get_user_info(current_user: Annotated[UserRead, Depends(get_current_user)]):
    return current_user
