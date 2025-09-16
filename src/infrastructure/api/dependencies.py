from sqlalchemy.orm import Session
from fastapi import Depends

from src.infrastructure.db.postgres import SessionLocal
from src.infrastructure.repositories.game_repository_impl import GameRepositoryImpl
from src.application.game_service import GameService

# ----- Database session dependency -----
def get_db():
    """
    Provides a SQLAlchemy database session.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- GameService dependency -----
def get_game_service(db: Session = Depends(get_db)) -> GameService:
    """
    Provides a GameService instance using the DB session.
    Injected into API routes via FastAPI Depends.
    """
    repo = GameRepositoryImpl(db)
    return GameService(repo, db)
