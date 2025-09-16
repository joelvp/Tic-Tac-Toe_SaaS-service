from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GameModel(Base):
    """SQLAlchemy model representing a Tic-Tac-Toe game in the database."""
    __tablename__ = "games"

    game_id = Column(String, primary_key=True, index=True)
    board = Column(JSONB, nullable=False)        # Board state: 3x3 list of "X", "O", or None
    next_player = Column(String, nullable=True)  # Next player: "X" or "O", None if game finished
    winner = Column(String, nullable=True)       # Winner: "X", "O" or None
    is_finished = Column(Boolean, default=False, nullable=False)
