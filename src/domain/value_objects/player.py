from enum import Enum
from src.domain.exceptions import InvalidPlayer

class Player(str, Enum):
    X = "X"
    O = "O"

    @staticmethod
    def from_str(value: str) -> "Player":
        try:
            return Player(value)
        except ValueError:
            raise InvalidPlayer(f"Invalid player, should be 'X' or 'O', got '{value}'")

    def opponent(self) -> "Player":
        return Player.O if self == Player.X else Player.X
