from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db import get_db

from typing import List
from app.models import User

from app.schemas.opening_schema import OpeningCreate, OpeningReadReduced
from app.services.opening_service import create_opening, get_openings_by_user
from app.services.auth_service import get_current_user

router = APIRouter()


# opening router
@router.post("/")
async def add_opening(opening: OpeningCreate, db: Session = Depends(get_db)):
    print("OC", opening)
    created_opening = create_opening(db=db, opening_create=opening)
    return created_opening


@router.get("/", response_model=List[OpeningReadReduced])
async def read_openings(db: Session = Depends(get_db)):
    openings: List[OpeningReadReduced] = get_openings_by_user(db, user_id=1)
    return openings
