from copy import deepcopy
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.models import Opening
from app.schemas.opening_schema import (
    OpeningCreate,
    OpeningUpdate,
    OpeningReadReduced,
    OpeningsList,
    Move,
)
from typing import List


def create_opening(db: Session, user_id: int, opening_create: OpeningCreate) -> Opening:
    db_opening = Opening(
        user_id=user_id,
        name=opening_create.name,
        data=opening_create.data.model_dump(),
    )
    db.add(db_opening)
    db.commit()
    db.refresh(db_opening)
    return db_opening


def get_openings_by_user(
    db: Session,
    user_id: int,
    name: str,
    skip: int = 0,
    limit: int = 10,
) -> OpeningsList:
    query = db.query(Opening).filter(Opening.user_id == user_id)
    if name:
        query = query.filter(Opening.name.ilike(f"%{name}%"))
    total_openings = query.count()
    openings = query.offset(skip).limit(limit).all()
    openings_reduced = [
        OpeningReadReduced(id=opening.id, name=opening.name) for opening in openings
    ]
    return {"total": total_openings, "openings": openings_reduced}


def get_user_opening_by_id(
    db: Session,
    user_id: int,
    id: int,
) -> Opening:
    opening = db.query(Opening).get(id)
    if not opening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opening no encontrado.",
        )
    if opening.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El opening no pertenece a este usuario.",
        )
    return opening


def delete_user_opening_by_id(db: Session, user_id: int, id: int) -> Opening:
    opening = get_user_opening_by_id(db=db, user_id=user_id, id=id)
    db.delete(opening)
    db.commit()
    return opening


def update_user_opening(
    db: Session, user_id: int, opening_id: int, opening_update: OpeningUpdate
) -> Opening:
    opening = get_user_opening_by_id(db, user_id, opening_id)
    if opening_update.name is not None:
        opening.name = opening_update.name
    if opening_update.data is not None:
        opening.data = opening_update.data.model_dump()
    db.commit()
    return opening


def compute_opening_after_move(
    opening: Opening, move: Move, move_name: str, path: List[str]
) -> Opening:
    opening_copy = deepcopy(opening)
    data = opening_copy.data
    for p in path:
        if p in data["moves"]:
            data = data["moves"][p]
        else:
            raise ValueError(f"Move '{p}' not found in the path.")
    data["moves"][move_name] = move
    return opening_copy
