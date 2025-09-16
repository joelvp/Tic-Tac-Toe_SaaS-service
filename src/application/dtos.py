from dataclasses import dataclass
from typing import Optional, List

@dataclass
class MoveResult:
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None

@dataclass
class GameStatus:
    game_id: str
    board: List[List[Optional[str]]]
    next_player: Optional[str]
    winner: Optional[str]
    is_finished: bool
