from sqlalchemy.orm import Session
from app.models import Opening
from app.schemas.opening_schema import OpeningCreate

from typing import List


def create_opening(db: Session, opening_create: OpeningCreate):
    db_opening = Opening(
        name=opening_create.name,
        user_id=opening_create.user_id,
        data=opening_create.data,
    )
    db.add(db_opening)
    db.commit()
    db.refresh(db_opening)
    return db_opening


def get_openings_by_user(db: Session, user_id: int) -> List[Opening]:
    return db.query(Opening).filter(Opening.user_id == user_id).all()
