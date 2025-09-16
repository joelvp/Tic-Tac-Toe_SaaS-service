import pytest
from src.domain.value_objects.position import Position
from src.domain.exceptions import InvalidMove

def test_valid_position():
    pos = Position(1, 3)
    assert pos.x == 1
    assert pos.y == 3

def test_invalid_position_x():
    with pytest.raises(InvalidMove):
        Position(0, 2)
    with pytest.raises(InvalidMove):
        Position(4, 2)

def test_invalid_position_y():
    with pytest.raises(InvalidMove):
        Position(2, 0)
    with pytest.raises(InvalidMove):
        Position(2, 4)

def test_zero_indexed():
    pos = Position(2, 3)
    assert pos.zero_indexed == (1, 2)

def test_equality():
    pos1 = Position(2, 2)
    pos2 = Position(2, 2)
    pos3 = Position(3, 2)
    assert pos1 == pos2
    assert pos1 != pos3
