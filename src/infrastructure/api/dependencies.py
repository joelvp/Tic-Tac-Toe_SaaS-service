from sqlalchemy.orm import Session
from fastapi import Depends
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.game_repository_impl import GameRepositoryImpl
from src.application.game_service import GameService


def get_game_service(db: Session = Depends(get_db)) -> GameService:
    """
    Provides a GameService instance using the DB session.
    Injected into API routes via FastAPI Depends.
    """
    repo = GameRepositoryImpl(db)
    return GameService(repo)
