from typing import Optional
from sqlalchemy.orm import Session
from src.infrastructure.db.models import GameModel
from src.domain.entities.game import Game
from src.domain.repositories.game_repository import GameRepository
from src.domain.value_objects.player import Player
from src.infrastructure.logging.logger import logger


class GameRepositoryImpl(GameRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, game: Game) -> None:
        """
        Inserts or updates a game in the database.
        Does not commit: the calling service should handle the transaction.
        """
        try:
            db_game = self._to_db_model(game)
            self.db.merge(db_game)
            logger.info(f"Game {game.game_id} merged into database.")
        except Exception as e:
            logger.error(f"Failed to add/merge game {game.game_id}: {e}", exc_info=True)
            raise

    def get(self, game_id: str) -> Optional[Game]:
        """
        Retrieves a game from the database and converts it into a domain entity.
        """
        try:
            db_game = self.db.query(GameModel).filter(GameModel.game_id == game_id).first()
            if not db_game:
                logger.warning(f"Game {game_id} not found in database.")
                return None
            game = self._from_db_model(db_game)
            logger.info(f"Game {game_id} retrieved from database.")
            return game
        except Exception as e:
            logger.error(f"Error retrieving game {game_id}: {e}", exc_info=True)
            raise

    # ----- Private conversion methods -----
    def _to_db_model(self, game: Game) -> GameModel:
        # Convert Player -> str
        board_as_str = [
            [cell.value if cell else None for cell in row]
            for row in game.board.grid
        ]
        return GameModel(
            game_id=game.game_id,
            board=board_as_str,
            next_player=game.next_player.value if game.next_player else None,
            winner=game.winner.value if game.winner else None,
            is_finished=game.is_finished
        )

    def _from_db_model(self, db_game: GameModel) -> Game:
        game = Game(db_game.game_id)
        # Convert str -> Player
        game.board.grid = [
            [Player(cell) if cell else None for cell in row]
            for row in db_game.board
        ]
        game.next_player = Player(db_game.next_player) if db_game.next_player else None
        game.winner = Player(db_game.winner) if db_game.winner else None
        game.is_finished = db_game.is_finished
        return game
