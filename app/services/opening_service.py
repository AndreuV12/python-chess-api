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
from app.services.stockfish_service import ChessAnalysisService
from typing import List


def create_opening(db: Session, user_id: int, opening_create: OpeningCreate) -> Opening:
    db_opening = Opening(
        user_id=user_id,
        name=opening_create.name,
        data=opening_create.data.model_dump(),
        color=opening_create.color,
        preview_fen=opening_create.preview_fen,
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
    openings_reduced = [OpeningReadReduced(**opening.__dict__) for opening in openings]
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
    opening: Opening, move: Move, path: List[str]
) -> Opening:
    opening_copy = deepcopy(opening)
    data = opening_copy.data
    for p in path:
        if p in data["moves"]:
            data = data["moves"][p]
        else:
            raise ValueError(f"Move '{p}' not found in the path.")
    stockfish = ChessAnalysisService()
    move.name = stockfish.get_move_name(data["fen"], move.uci)
    move.analysis = stockfish.analyze_position(move.fen, depth=16)
    data["moves"][move.uci] = move
    return opening_copy


def compute_opening_after_delete_move(
    opening: Opening, move: Move, path: List[str]
) -> Opening:
    opening_copy = deepcopy(opening)
    data = opening_copy.data
    for p in path:
        if p in data["moves"]:
            data = data["moves"][p]
        else:
            raise ValueError(f"Move '{p}' not found in the path.")
    if move.uci in data["moves"]:
        del data["moves"][move.uci]
    else:
        raise ValueError(f"Move '{move.uci}' not found in the current position.")
    return opening_copy
