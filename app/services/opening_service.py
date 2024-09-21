from sqlalchemy.orm import Session
from app.models import Opening
from app.schemas.opening_schema import OpeningCreate

from typing import List


def create_opening(db: Session, opening_create: OpeningCreate, user_id: int) -> Opening:
    db_opening = Opening(
        user_id=user_id,
        name=opening_create.name,
        data=opening_create.model_dump()["data"],
    )
    db.add(db_opening)
    db.commit()
    db.refresh(db_opening)
    return db_opening


def get_openings_by_user(db: Session, user_id: int) -> List[Opening]:
    return db.query(Opening).filter(Opening.user_id == user_id).all()


def get_opening_by_id(db: Session, id: int) -> Opening:
    return db.query(Opening).get(id)


def delete_opening_by_id(db: Session, id: int) -> bool:
    opening = db.query(Opening).get(id)
    if not opening:
        return False
    db.delete(opening)
    db.commit()
    return opening
