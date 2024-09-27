from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class Analysis(BaseModel):
    score: int
    source: str


class Move(BaseModel):
    fen: str
    uci: Optional[str] = None
    name: Optional[str] = None
    analysis: Optional[Analysis] = None
    moves: Dict[str, "Move"] = Field(default_factory=dict)


class OpeningRead(BaseModel):
    id: int
    name: str
    data: Move


class OpeningReadReduced(BaseModel):
    id: int
    name: str


class OpeningsList(BaseModel):
    openings: List[OpeningReadReduced]
    total: int


class OpeningCreate(BaseModel):
    name: str
    data: Move = Move(
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", moves={}
    )


class OpeningUpdate(BaseModel):
    name: Optional[str] = None
    data: Optional[Move] = None


class AddMoveRequest(BaseModel):
    move: Move
    path: List[str]
