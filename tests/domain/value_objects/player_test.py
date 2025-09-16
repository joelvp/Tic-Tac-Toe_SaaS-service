import pytest
from src.domain.value_objects.player import Player
from src.domain.exceptions import InvalidPlayer

def test_player_enum_values():
    assert Player.X.value == "X"
    assert Player.O.value == "O"

def test_from_str_valid():
    assert Player.from_str("X") == Player.X
    assert Player.from_str("O") == Player.O

def test_from_str_invalid():
    with pytest.raises(InvalidPlayer):
        Player.from_str("A")

def test_opponent_method():
    assert Player.X.opponent() == Player.O
    assert Player.O.opponent() == Player.X
