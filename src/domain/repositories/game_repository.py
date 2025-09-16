from abc import ABC, abstractmethod
from src.domain.entities.game import Game

class GameRepository(ABC):
    """Abstract repository interface for Game entity."""

    @abstractmethod
    def add(self, game: Game):
        """Add or update a game in the repository."""
        pass

    @abstractmethod
    def get(self, game_id: str) -> Game:
        """Retrieve a game by its ID. Return None if not found."""
        pass
