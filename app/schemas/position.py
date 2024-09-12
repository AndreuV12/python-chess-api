from typing import Dict
from pydantic import BaseModel
from .piece import ChessPiece  # Importar el modelo ChessPiece

from enum import Enum


class Coordinade(str, Enum):
    A1 = "a1"
    B1 = "b1"
    C1 = "c1"
    D1 = "d1"
    E1 = "e1"
    F1 = "f1"
    G1 = "g1"
    H1 = "h1"

    A2 = "a2"
    B2 = "b2"
    C2 = "c2"
    D2 = "d2"
    E2 = "e2"
    F2 = "f2"
    G2 = "g2"
    H2 = "h2"

    A3 = "a3"
    B3 = "b3"
    C3 = "c3"
    D3 = "d3"
    E3 = "e3"
    F3 = "f3"
    G3 = "g3"
    H3 = "h3"

    A4 = "a4"
    B4 = "b4"
    C4 = "c4"
    D4 = "d4"
    E4 = "e4"
    F4 = "f4"
    G4 = "g4"
    H4 = "h4"

    A5 = "a5"
    B5 = "b5"
    C5 = "c5"
    D5 = "d5"
    E5 = "e5"
    F5 = "f5"
    G5 = "g5"
    H5 = "h5"

    A6 = "a6"
    B6 = "b6"
    C6 = "c6"
    D6 = "d6"
    E6 = "e6"
    F6 = "f6"
    G6 = "g6"
    H6 = "h6"

    A7 = "a7"
    B7 = "b7"
    C7 = "c7"
    D7 = "d7"
    E7 = "e7"
    F7 = "f7"
    G7 = "g7"
    H7 = "h7"

    A8 = "a8"
    B8 = "b8"
    C8 = "c8"
    D8 = "d8"
    E8 = "e8"
    F8 = "f8"
    G8 = "g8"
    H8 = "h8"


class Position(BaseModel):
    position: Dict[Coordinade, ChessPiece] = {}

    def add_piece(self, position: str, piece: ChessPiece):
        """Agregar una pieza en la posición dada"""
        if position in self.pieces:
            raise ValueError(f"Ya hay una pieza en {position}: {self.pieces[position]}")
        self.pieces[position] = piece

    def move_piece(self, from_position: str, to_position: str):
        """Mover una pieza de una posición a otra"""
        if from_position not in self.pieces:
            raise ValueError(f"No hay pieza en {from_position}")
        piece = self.pieces.pop(from_position)
        self.pieces[to_position] = piece

    def __repr__(self):
        return "\n".join(
            f"{position}: {piece}" for position, piece in self.pieces.items()
        )
