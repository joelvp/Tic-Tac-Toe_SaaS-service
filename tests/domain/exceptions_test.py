from src.domain.exceptions import InvalidMove, GameFinished, InvalidPlayer

def test_invalid_move_exception():
    try:
        raise InvalidMove("Invalid move")
    except InvalidMove as e:
        assert str(e) == "Invalid move"

def test_game_finished_exception():
    try:
        raise GameFinished("Game finished")
    except GameFinished as e:
        assert str(e) == "Game finished"

def test_invalid_player_exception():
    try:
        raise InvalidPlayer("Invalid player")
    except InvalidPlayer as e:
        assert str(e) == "Invalid player"
