from abc import ABC, abstractmethod
from src.domain.entities.game import Game

class GameRepository(ABC):
    @abstractmethod
    def add(self, game: Game):
        pass

    @abstractmethod
    def get(self, game_id: str) -> Game:
        pass
