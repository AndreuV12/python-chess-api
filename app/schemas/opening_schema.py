from pydantic import BaseModel
from typing import Dict, Optional


class Move(BaseModel):
    fen: str
    moves: Optional[Dict[str, "Move"]] = {}


class OpeningRead(BaseModel):
    id: int
    name: str
    data: Move


class OpeningReadReduced(BaseModel):
    id: int
    name: str


class OpeningCreate(BaseModel):
    name: str
    data: Move = Move(
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", moves={}
    )
