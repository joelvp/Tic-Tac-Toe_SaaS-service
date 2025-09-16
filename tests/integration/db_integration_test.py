import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.infrastructure.db.models import Base
from src.infrastructure.repositories.game_repository_impl import GameRepositoryImpl
from src.application.game_service import GameService
from src.domain.entities.game import Game
from src.domain.value_objects.player import Player
from src.application.dtos import MoveResult


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
def game():
    g = Game("game123")
    g.board.grid[0][0] = Player.X
    g.next_player = Player.O
    g.winner = None
    g.is_finished = False
    return g

def test_add_and_get_game(repo, game):
    repo.add(game)
    result = repo.get(game.game_id)
    assert result is not None
    assert result.game_id == game.game_id
    assert result.board.grid[0][0] == game.board.grid[0][0]

def test_add_multiple_games(repo):
    g1 = Game("game1")
    g2 = Game("game2")
    repo.add(g1)
    repo.add(g2)
    assert repo.get("game1") is not None
    assert repo.get("game2") is not None

def test_create_game(service):
    game_id = service.create_game()
    status = service.get_status(game_id)
    assert status is not None
    assert status.game_id == game_id
    assert not status.is_finished
    assert status.next_player in ("X", "O")

def test_play_move_valid(service):
    game_id = service.create_game()
    result = service.play_move(game_id, "X", 1, 1)
    assert isinstance(result, MoveResult)
    assert result.success
    status = service.get_status(game_id)
    assert status.board[0][0] == "X"
    assert status.next_player == "O"

def test_play_move_out_of_turn(service):
    game_id = service.create_game()
    result = service.play_move(game_id, "O", 1, 1)
    assert not result.success
    assert "turn" in result.error.lower()

def test_full_game_draw(service):
    game_id = service.create_game()
    moves = [
        ("X", 1, 1), ("O", 1, 2),
        ("X", 1, 3), ("O", 2, 2),
        ("X", 2, 1), ("O", 2, 3),
        ("X", 3, 2), ("O", 3, 1),
        ("X", 3, 3)
    ]
    last_result = None
    for player, x, y in moves:
        last_result = service.play_move(game_id, player, x, y)
    assert last_result.success
    assert "draw" in last_result.message.lower()
    status = service.get_status(game_id)
    assert status.is_finished
    assert status.winner is None

def test_full_game_win(service):
    game_id = service.create_game()
    moves = [
        ("X", 1, 1), ("O", 2, 1),
        ("X", 1, 2), ("O", 2, 2),
        ("X", 1, 3)
    ]
    last_result = None
    for player, x, y in moves:
        last_result = service.play_move(game_id, player, x, y)
    assert last_result.success
    assert "won" in last_result.message.lower()
    status = service.get_status(game_id)
    assert status.is_finished
    assert status.winner == "X"
