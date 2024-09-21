from pydantic import BaseModel
from typing import Dict, Optional, List, Any
import json


class Move(BaseModel):
    fen: str
    moves: Optional[Dict[str, "Move"]] = {}


class OpeningRead(BaseModel):
    id: int
    name: str
    data: Dict[str, "Move"]


class OpeningReadReduced(BaseModel):
    id: int
    name: str


class OpeningCreate(BaseModel):
    name: str
    data: Dict[str, "Move"] = {}
