from pydantic import BaseModel, field_validator, ValidationError
from typing import Dict, Optional, List
import json
import re


class Move(BaseModel):
    fen: str
    moves: Optional[Dict[str, "Move"]] = {}


class OpeningRead(BaseModel):
    id: int
    name: str
    data: Optional[Dict[str, "Move"]]

    def __str__(self) -> str:
        return json.dumps(self.dict(), indent=4)


class OpeningsRead(BaseModel):
    openings: List[OpeningRead]


move_d4 = {
    "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1",
    "moves": {
        "D8D5": {"fen": "'rnbqkbnr/pppppppp/8/4P3/4p3/8/PPPP1PPP/RNBQKBNR w KQkq - 0'"},
        "D7D6": {
            "fen": "'rnbqkbnr/pppppppp/8/4P3/4p3/8/PPPP1PPP/RNBQKBNR w KQkq - 0'",
            "moves": {
                "D4D5": {"fen": "FEN"},
            },
            "Otra cosa": "aaa",
        },
    },
}

data = {"D2D4": move_d4}

opening = OpeningRead(id=1, name="Game 1", data=data)
openings_read = OpeningsRead(openings=[opening])
print(str(opening))
