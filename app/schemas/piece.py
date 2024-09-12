from pydantic import BaseModel
from enum import Enum


class PieceName(str, Enum):
    KING = "K"
    QUEEN = "Q"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    PAWN = "P"


class PieceColor(str, Enum):
    WHITE = "W"
    BLACK = "B"


class ChessPiece(BaseModel):
    name: PieceName
    color: PieceColor
