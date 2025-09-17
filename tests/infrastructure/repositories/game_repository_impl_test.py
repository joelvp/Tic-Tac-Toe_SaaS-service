import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.repositories.game_repository_impl import GameRepositoryImpl
from src.domain.entities.game import Game
from src.domain.value_objects.player import Player

@pytest.fixture
def db_session():
    return MagicMock()

@pytest.fixture
def repo(db_session):
    return GameRepositoryImpl(db_session)

@pytest.fixture
def game():
    g = Game("game123")
    g.board.grid[0][0] = Player.X
    g.next_player = Player.O
    g.winner = None
    g.is_finished = False
    return g

def test_add_merges_game(repo, db_session, game):
    repo._to_db_model = MagicMock(return_value="db_game")
    db_session.merge.return_value = None
    repo.add(game)
    repo._to_db_model.assert_called_with(game)
    db_session.merge.assert_called_with("db_game")
    db_session.commit.assert_called()

def test_add_logs_and_raises_on_error(repo, game):
    repo._to_db_model = MagicMock(side_effect=Exception("fail"))
    with patch("src.infrastructure.repositories.game_repository_impl.logger") as logger_mock:
        with pytest.raises(Exception):
            repo.add(game)
        logger_mock.error.assert_called()

    assert not repo.db.commit.called

def test_get_returns_none_if_not_found(repo):
    repo.db.query().filter().first.return_value = None
    with patch("src.infrastructure.repositories.game_repository_impl.logger") as logger_mock:
        result = repo.get("bad_id")
        assert result is None
        logger_mock.warning.assert_called()

def test_get_returns_game_if_found(repo, game):
    db_game = MagicMock()
    repo.db.query().filter().first.return_value = db_game
    repo._from_db_model = MagicMock(return_value=game)
    with patch("src.infrastructure.repositories.game_repository_impl.logger") as logger_mock:
        result = repo.get("game123")
        assert result == game
        repo._from_db_model.assert_called_with(db_game)
        logger_mock.info.assert_called()

def test_get_logs_and_raises_on_error(repo):
    repo.db.query().filter().first.side_effect = Exception("fail")
    with patch("src.infrastructure.repositories.game_repository_impl.logger") as logger_mock:
        with pytest.raises(Exception):
            repo.get("game123")
        logger_mock.error.assert_called()

def test_to_db_model_and_from_db_model(repo, game):
    db_model = repo._to_db_model(game)
    assert db_model.game_id == game.game_id
    assert db_model.board[0][0] == game.board.grid[0][0].value

    new_game = repo._from_db_model(db_model)
    assert new_game.game_id == game.game_id
    assert new_game.board.grid[0][0] == game.board.grid[0][0]
