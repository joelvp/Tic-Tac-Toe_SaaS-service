from fastapi import APIRouter, HTTPException, Depends
from src.infrastructure.api.dependencies import get_game_service
from src.infrastructure.api.dtos import MoveRequest
from src.infrastructure.logging.logger import logger
from src.application.game_service import GameService  # for typing

router = APIRouter()


@router.post("/create")
def create_game(service: GameService = Depends(get_game_service)):
    """Create a new game and return its unique ID."""
    logger.info("POST /games/create called")
    game_id = service.create_game()
    return {"gameId": game_id}


@router.post("/move")
def move(request: MoveRequest, service: GameService = Depends(get_game_service)):
    """Play a move in a given game."""
    logger.info(
        f"POST /games/move called with gameId={request.gameId}, "
        f"playerId={request.playerId}, square=({request.square.x},{request.square.y})"
    )
    result = service.play_move(
        request.gameId,
        request.playerId,
        request.square.x,
        request.square.y
    )
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return {"status": result.message}


@router.get("/status")
def status(game_id: str, service: GameService = Depends(get_game_service)):
    """Fetch the current status of a game."""
    logger.info(f"GET /games/status called with gameId={game_id}")
    result = service.get_status(game_id)
    if not result:
        raise HTTPException(status_code=404, detail="Game not found")
    return result
