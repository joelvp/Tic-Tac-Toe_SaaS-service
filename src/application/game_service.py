import uuid
from typing import Optional
from sqlalchemy.orm import Session

from src.domain.entities.game import Game
from src.domain.repositories.game_repository import GameRepository
from src.domain.value_objects.player import Player
from src.domain.value_objects.position import Position
from src.domain.exceptions import InvalidMove, GameFinished, InvalidPlayer
from src.application.dtos import MoveResult, GameStatus
from src.infrastructure.logging.logger import logger


class GameService:
    def __init__(self, repo: GameRepository, db_session: Session):
        self.repo = repo
        self.db: Session = db_session

    def create_game(self) -> str:
        game_id = str(uuid.uuid4())
        game = Game(game_id)
        self.repo.add(game)
        self.db.commit()
        logger.info(f"Game created successfully: {game_id}")
        return game_id

    def play_move(self, game_id: str, player_id: str, x: int, y: int) -> MoveResult:
        logger.debug(f"Attempting move: game_id={game_id}, player_id={player_id}, x={x}, y={y}")
        game = self.repo.get(game_id)
        if not game:
            logger.warning(f"Game not found: {game_id}")
            return MoveResult(success=False, error="Game not found")

        try:
            player = Player.from_str(player_id)
        except InvalidPlayer as e:
            logger.warning(f"Invalid player attempted to move: {player_id} in game {game_id}")
            return MoveResult(success=False, error=str(e))

        if game.next_player is None or game.next_player != player:
            logger.warning(f"Player {player_id} tried to move out of turn in game {game_id}")
            return MoveResult(success=False, error="It's not your turn")

        try:
            position = Position(x, y)
            game.play_move(position)
            self.repo.add(game)
            self.db.commit()

            if game.is_finished:
                if game.winner:
                    message = f"Player {game.winner.value} has won!"
                    logger.info(f"Game finished: {game_id}, winner={game.winner.value}")
                else:
                    message = "The game is a draw"
                    logger.info(f"Game finished as a draw: {game_id}")
            else:
                message = f"Move registered, next player is {game.next_player.value}"
                logger.info(f"Move registered: game_id={game_id}, next_player={game.next_player.value}")

            return MoveResult(success=True, message=message)

        except (InvalidMove, GameFinished) as e:
            self.db.rollback()
            logger.error(f"Error during move in game {game_id}: {str(e)}")
            return MoveResult(success=False, error=str(e))

    def get_status(self, game_id: str) -> Optional[GameStatus]:
        logger.debug(f"Fetching status for game_id={game_id}")
        game = self.repo.get(game_id)
        if not game:
            logger.warning(f"Game not found when fetching status: {game_id}")
            return None

        status = GameStatus(
            game_id=game.game_id,
            board=[[cell.value if cell else None for cell in row] for row in game.board.grid],
            next_player=game.next_player.value if not game.is_finished else None,
            winner=game.winner.value if game.winner else None,
            is_finished=game.is_finished
        )
        logger.debug(f"Status fetched for game_id={game_id}: {status}")
        return status
