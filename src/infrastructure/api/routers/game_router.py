from fastapi import APIRouter, HTTPException, Depends
from src.infrastructure.api.dependencies import get_game_service
from src.infrastructure.api.dtos import MoveRequest
from src.infrastructure.logging.logger import logger 

router = APIRouter()

@router.post("/create")
def create_game(service=Depends(get_game_service)):
    logger.info("POST /games/create called")
    gameId = service.create_game()
    return {"gameId": gameId}

@router.post("/move")
def move(request: MoveRequest, service=Depends(get_game_service)):
    logger.info(f"POST /games/move called with gameId={request.gameId}, playerId={request.playerId}, square=({request.square.x},{request.square.y})")
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
def status(gameId: str, service=Depends(get_game_service)):
    logger.info(f"GET /games/status called with gameId={gameId}")
    result = service.get_status(gameId)
    if not result:
        raise HTTPException(status_code=404, detail="Game not found")
    return result
