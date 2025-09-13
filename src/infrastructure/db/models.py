from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GameModel(Base):
    __tablename__ = "games"

    game_id = Column(String, primary_key=True, index=True)
    board = Column(JSONB, nullable=False)  # lista de listas con "X", "O" o None
    next_player = Column(String, nullable=True)  # "X" o "O"
    winner = Column(String, nullable=True)      # "X", "O" o None
    is_finished = Column(Boolean, default=False, nullable=False)
