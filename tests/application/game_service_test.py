import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.application.game_service import GameService
from src.domain.value_objects.player import Player
from src.domain.entities.game import Game
from src.domain.value_objects.position import Position
from src.application.dtos import MoveResult, GameStatus


@pytest.fixture
def db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def repo():
    return MagicMock()

@pytest.fixture
def service(repo, db_session):
    return GameService(repo, db_session)
    return GameService(repo, db_session)

@pytest.fixture
def game():
    return Game("game123")

@pytest.fixture
def game_x_turn(game):
    game.next_player = Player.X
    return game

def mark_cell(game, x, y, player=Player.X):
    game.next_player = player
    game.play_move(Position(x, y))

def test_create_game(service, repo, db_session):
    repo.add.return_value = None
    db_session.commit.return_value = None
    game_id = service.create_game()
    assert isinstance(game_id, str)
    repo.add.assert_called()
    db_session.commit.assert_called()

def test_play_move_success(service, repo, game_x_turn, db_session):
    repo.get.return_value = game_x_turn
    result = service.play_move("game123", "X", 1, 1)
    assert result.success is True
    assert "Move registered" in result.message or "has won" in result.message or "draw" in result.message
    repo.add.assert_called()
    db_session.commit.assert_called()

def test_play_move_winner_branch(service, repo, game_x_turn, db_session):
    game = game_x_turn

    # Mock play_move to force a win
    def fake_play_move(position):
        game.is_finished = True
        game.winner = Player.X

    game.play_move = fake_play_move
    repo.get.return_value = game

    result = service.play_move("game123", "X", 1, 1)
    assert result.success is True
    assert "has won" in result.message
    db_session.commit.assert_called()

def test_play_move_draw_branch(service, repo, game_x_turn, db_session):
    game = game_x_turn

    # Simulate a move that ends in a draw
    def fake_play_move(position):
        game.is_finished = True
        game.winner = None

    game.play_move = fake_play_move
    repo.get.return_value = game

    result = service.play_move("game123", "X", 1, 1)
    assert result.success is True
    assert "draw" in result.message
    db_session.commit.assert_called()

def test_play_move_game_not_found(service, repo):
    repo.get.return_value = None
    result = service.play_move("bad_id", "X", 1, 1)
    assert result.success is False
    assert result.error == "Game not found"

def test_play_move_invalid_player(service, repo, game):
    repo.get.return_value = game
    result = service.play_move("game123", "A", 1, 1)
    assert result.success is False
    assert "Invalid player" in result.error

def test_play_move_out_of_turn(service, repo, game):
    game.next_player = Player.O
    repo.get.return_value = game
    result = service.play_move("game123", "X", 1, 1)
    assert result.success is False
    assert result.error == "It's not your turn"

def test_play_move_invalid_move(service, repo, game, db_session):
    repo.get.return_value = game
    # Mark the cell first
    mark_cell(game, 1, 1)
    # Try to mark again with the other player
    result = service.play_move("game123", "O", 1, 1)
    assert result.success is False
    assert "already taken" in result.error or "Error" in result.error
    db_session.rollback.assert_called()

def test_get_status_success(service, repo, game):
    repo.get.return_value = game
    status_result = service.get_status("game123")
    assert isinstance(status_result, GameStatus)
    assert status_result.game_id == "game123"
    assert status_result.board is not None

def test_get_status_game_not_found(service, repo):
    repo.get.return_value = None
    status_result = service.get_status("bad_id")
    assert status_result is None
