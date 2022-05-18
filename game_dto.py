from typing import Optional
from pydantic import BaseModel
from enum import Enum

class Game(BaseModel):
    id: Optional[str] = None
    board:  Optional[str] = None
    status:  Optional[str] = None


class CreatGame(BaseModel):
    board: str

class UpdateGame(BaseModel):
    board: str

class Status(Enum):
    RUNNING = 10
    O_WON = 20
    X_WON = 30
    DRAW = 40