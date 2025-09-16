import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.infrastructure.db.models import Base
from src.infrastructure.repositories.game_repository_impl import GameRepositoryImpl
from src.application.game_service import GameService
from src.infrastructure.api.routers import game_router

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def db_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def repo(db_session):
    return GameRepositoryImpl(db_session)

@pytest.fixture
def service(repo, db_session):
    return GameService(repo, db_session)

@pytest.fixture
def app(service):
    app = FastAPI()
    app.include_router(game_router.router, prefix="/games")
    app.dependency_overrides[game_router.get_game_service] = lambda: service
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

def test_create_game_endpoint(client):
    response = client.post("/games/create")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "gameId" in data and len(data["gameId"]) > 0

def test_move_endpoint(client):
    game_id = client.post("/games/create").json()["gameId"]
    payload = {"gameId": game_id, "playerId": "X", "square": {"x": 1, "y": 1}}
    response = client.post("/games/move", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert "Move registered" in response.json().get("status", "")

def test_status_endpoint(client):
    game_id = client.post("/games/create").json()["gameId"]
    client.post("/games/move", json={"gameId": game_id, "playerId": "X", "square": {"x": 1, "y": 1}})
    response = client.get("/games/status", params={"game_id": game_id})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["game_id"] == game_id
    assert data["board"][0][0] == "X"
    assert data["next_player"] == "O"

def test_move_invalid_square(client):
    game_id = client.post("/games/create").json()["gameId"]
    payload = {"gameId": game_id, "playerId": "X", "square": {"x": 4, "y": 2}}
    response = client.post("/games/move", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Position 4,2 out of board range (1-3)" in response.json()["detail"]

def test_move_wrong_player(client):
    game_id = client.post("/games/create").json()["gameId"]
    client.post("/games/move", json={"gameId": game_id, "playerId": "X", "square": {"x": 1, "y": 1}})
    response = client.post("/games/move", json={"gameId": game_id, "playerId": "X", "square": {"x": 1, "y": 2}})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "It's not your turn" in response.json()["detail"]

def test_status_game_not_found(client):
    response = client.get("/games/status", params={"game_id": "nonexistent"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Game not found" in response.json()["detail"]
