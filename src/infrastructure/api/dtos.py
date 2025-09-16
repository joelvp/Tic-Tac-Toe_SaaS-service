from pydantic import BaseModel

class PositionRequest(BaseModel):
    x: int
    y: int

class MoveRequest(BaseModel):
    gameId: str
    playerId: str
    square: PositionRequest
