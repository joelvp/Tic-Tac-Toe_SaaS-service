from fastapi import FastAPI
from src.infrastructure.db.postgres import engine
from src.infrastructure.db.models import Base
from src.infrastructure.api.routers.game_router import router as game_router
from src.infrastructure.logging.logger import logger

app = FastAPI(title="Tic-Tac-Toe API")

@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.exception("Failed to initialize database tables: %s", e)
        raise

# Registrar routers
app.include_router(game_router, prefix="/games", tags=["games"])
logger.info("Game router registered under /games")
