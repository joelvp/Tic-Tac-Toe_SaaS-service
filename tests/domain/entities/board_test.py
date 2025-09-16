import pytest
from src.domain.entities.board import Board
from src.domain.value_objects.player import Player
from src.domain.value_objects.position import Position


@pytest.fixture
def board():
    return Board()

@pytest.fixture
def player_x():
    return Player("X")

@pytest.fixture
def player_o():
    return Player("O")

def test_mark_empty_cell(board, player_x):
    position = Position(1, 1)
    assert board.mark(player_x, position) is True
    assert board.grid[0][0] == player_x

def test_mark_occupied_cell(board, player_x):
    position = Position(1, 1)
    board.mark(player_x, position)
    assert board.mark(player_x, position) is False

def test_check_winner_row(board, player_x):
    for x in range(1, 4):
        board.mark(player_x, Position(x, 1))
    assert board.check_winner(player_x) is True

def test_check_winner_column(board, player_o):
    for y in range(1, 4):
        board.mark(player_o, Position(2, y))
    assert board.check_winner(player_o) is True

def test_check_winner_diagonal(board, player_x):
    for i in range(1, 4):
        board.mark(player_x, Position(i, i))
    assert board.check_winner(player_x) is True

def test_check_winner_anti_diagonal(board, player_o):
    for i in range(1, 4):
        board.mark(player_o, Position(4 - i, i))
    assert board.check_winner(player_o) is True

def test_is_full(board, player_x, player_o):
    moves = [
        (1, 1, player_x), (1, 2, player_o), (1, 3, player_x),
        (2, 1, player_o), (2, 2, player_x), (2, 3, player_o),
        (3, 1, player_x), (3, 2, player_o), (3, 3, player_x),
    ]
    for x, y, player in moves:
        board.mark(player, Position(x, y))
    assert board.is_full() is True

def test_str_representation(board, player_x):
    board.mark(player_x, Position(1, 1))
    result = str(board)
    assert "X" in result
