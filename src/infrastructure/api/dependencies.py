from sqlalchemy.orm import Session
from fastapi import Depends

from src.infrastructure.db.postgres import SessionLocal
from src.infrastructure.repositories.game_repository_impl import GameRepositoryImpl
from src.application.game_service import GameService

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GameService dependency
def get_game_service(db: Session = Depends(get_db)):
    repo = GameRepositoryImpl(db)
    return GameService(repo, db)
