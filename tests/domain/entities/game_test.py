import pytest
from src.domain.entities.game import Game
from src.domain.value_objects.position import Position
from src.domain.value_objects.player import Player
from src.domain.exceptions import InvalidMove, GameFinished

@pytest.fixture
def game():
    return Game(game_id="test123")

@pytest.fixture
def player_x():
    return Player.X

@pytest.fixture
def player_o():
    return Player.O

def test_first_move_sets_board_and_next_player(game):
    pos = Position(1, 1)
    game.play_move(pos)
    assert game.board.grid[0][0] == Player.X
    assert game.next_player == Player.O

def test_alternate_players(game):
    game.play_move(Position(1, 1))
    game.play_move(Position(2, 1))
    assert game.board.grid[0][1] == Player.O
    assert game.next_player == Player.X

def test_invalid_move_raises(game):
    game.play_move(Position(1, 1))
    with pytest.raises(InvalidMove):
        game.play_move(Position(1, 1))

def test_game_finished_raises(game):
    # Fill a row for Player.X to win
    game.play_move(Position(1, 1))  # X
    game.play_move(Position(1, 2))  # O
    game.play_move(Position(2, 1))  # X
    game.play_move(Position(2, 2))  # O
    game.play_move(Position(3, 1))  # X wins
    assert game.is_finished is True
    with pytest.raises(GameFinished):
        game.play_move(Position(3, 2))

def test_winner_detected(game):
    game.play_move(Position(1, 1))  # X
    game.play_move(Position(1, 2))  # O
    game.play_move(Position(2, 1))  # X
    game.play_move(Position(2, 2))  # O
    game.play_move(Position(3, 1))  # X wins
    assert game.winner == Player.X
    assert game.is_finished is True

def test_draw(game):
    moves = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 3), (2, 2),
        (3, 2), (3, 3), (3, 1)
    ]
    for x, y in moves:
        game.play_move(Position(x, y))

    assert game.is_finished is True
    assert game.winner is None
