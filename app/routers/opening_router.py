from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user

from typing import List

from app.schemas.user_schema import UserRead
from app.schemas.opening_schema import OpeningCreate, OpeningRead, OpeningReadReduced

from app.services.opening_service import (
    create_opening,
    get_openings_by_user,
    get_opening_by_id,
    delete_opening_by_id,
)

router = APIRouter()


# opening router
@router.post("/", response_model=OpeningRead)
async def add_opening(
    opening: OpeningCreate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    created_opening = create_opening(
        db=db, opening_create=opening, user_id=current_user.id
    )
    return created_opening


@router.get("/", response_model=List[OpeningReadReduced])
async def read_user_openings(
    db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)
):
    openings: List[OpeningReadReduced] = get_openings_by_user(db, current_user.id)
    return openings


@router.get("/{id}", response_model=OpeningRead)
async def read_user_opening_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    opening: OpeningRead = get_opening_by_id(db, id)
    if not opening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opening no encontrado.",
        )
    if opening.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El opening no pertenece a este usuario.",
        )
    return opening


@router.delete("/{id}", response_model=OpeningRead)
async def delete_user_opening_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    opening: OpeningRead = get_opening_by_id(db, id)
    if not opening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opening no encontrado.",
        )
    if opening.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El opening no pertenece a este usuario.",
        )
    delete_opening_by_id(db, id)
    return opening
