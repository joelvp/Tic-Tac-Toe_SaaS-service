from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from unittest.mock import MagicMock
import pytest

from src.infrastructure.api.routers import game_router

@pytest.fixture
def mock_service():
    return MagicMock()

@pytest.fixture
def app(mock_service):
    app = FastAPI()
    app.include_router(game_router.router, prefix="/games")
    app.dependency_overrides[game_router.get_game_service] = lambda: mock_service
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

def test_create_game(client, mock_service):
    mock_service.create_game.return_value = "game123"
    response = client.post("/games/create")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"gameId": "game123"}
    mock_service.create_game.assert_called_once()

def test_move_success(client, mock_service):
    move_result = MagicMock()
    move_result.success = True
    move_result.message = "Move registered"
    mock_service.play_move.return_value = move_result

    payload = {"gameId": "game123", "playerId": "X", "square": {"x": 1, "y": 1}}
    response = client.post("/games/move", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Move registered"}
    mock_service.play_move.assert_called_once_with("game123", "X", 1, 1)

def test_move_failure(client, mock_service):
    move_result = MagicMock()
    move_result.success = False
    move_result.error = "Invalid move"
    mock_service.play_move.return_value = move_result

    payload = {"gameId": "game123", "playerId": "X", "square": {"x": 1, "y": 1}}
    response = client.post("/games/move", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid move"

def test_status_success(client, mock_service):
    mock_service.get_status.return_value = {"game_id": "game123", "board": [[None]*3 for _ in range(3)]}
    response = client.get("/games/status", params={"game_id": "game123"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["game_id"] == "game123"
    mock_service.get_status.assert_called_once_with("game123")

def test_status_not_found(client, mock_service):
    mock_service.get_status.return_value = None
    response = client.get("/games/status", params={"game_id": "bad_id"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Game not found"
