from pydantic import BaseModel
from typing import Dict, Optional, List
import json


class Move(BaseModel):
    fen: str
    moves: Optional[Dict[str, "Move"]] = {}


class OpeningRead(BaseModel):
    id: int
    name: str
    data: Dict[str, "Move"]

    # def __str__(self) -> str:
    #     return json.dumps(self.model_dump(), indent=4)


class OpeningReadReduced(BaseModel):
    id: int
    name: str


class OpeningCreate(BaseModel):
    name: str
    user_id: int
    data: Dict[str, "Move"] = {}
