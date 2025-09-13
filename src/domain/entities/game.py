from src.domain.entities.board import Board
from src.domain.value_objects.player import Player
from src.domain.value_objects.position import Position
from src.domain.exceptions import InvalidMove, GameFinished

class Game:
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.board = Board()
        self.next_player: Player = Player.X  # X siempre empieza
        self.winner: Player | None = None
        self.is_finished: bool = False

    def play_move(self, position: Position):
        if self.is_finished:
            raise GameFinished("The game has already finished")

        if not self.board.mark(self.next_player, position):
            raise InvalidMove(f"Cell {position.x},{position.y} is already taken")

        if self.board.check_winner(self.next_player):
            self.winner = self.next_player
            self.is_finished = True
        elif self.board.is_full():
            self.winner = None
            self.is_finished = True
        else:
            self.next_player = self.next_player.opponent()
