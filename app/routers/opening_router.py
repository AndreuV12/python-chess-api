from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user

from typing import List

from app.schemas.user_schema import UserRead
from app.schemas.opening_schema import OpeningCreate, OpeningRead, OpeningReadReduced

from app.services.opening_service import create_opening, get_openings_by_user

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
async def read_openings(
    db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)
):
    openings: List[OpeningReadReduced] = get_openings_by_user(db, current_user.id)
    return openings
