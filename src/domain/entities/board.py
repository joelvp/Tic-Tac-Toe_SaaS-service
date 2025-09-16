from typing import Optional
from src.domain.value_objects.player import Player
from src.domain.value_objects.position import Position

class Board:
    def __init__(self):
        # 3x3 grid initialized with None
        self.grid: list[list[Optional[Player]]] = [[None]*3 for _ in range(3)]

    def mark(self, player: Player, position: Position) -> bool:
        """Mark the given position with the player if empty. Return True if successful."""
        x_idx, y_idx = position.zero_indexed
        if self.grid[y_idx][x_idx] is None:
            self.grid[y_idx][x_idx] = player
            return True
        return False

    def check_winner(self, player: Player) -> bool:
        """Check if the given player has won."""
        g = self.grid
        # Rows
        for row in g:
            if all(cell == player for cell in row):
                return True
        # Columns
        for col in range(3):
            if all(g[row][col] == player for row in range(3)):
                return True
        # Diagonals
        if all(g[i][i] == player for i in range(3)):
            return True
        if all(g[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_full(self) -> bool:
        """Return True if all cells are filled."""
        return all(all(cell is not None for cell in row) for row in self.grid)

    def __str__(self):
        # Simple visual representation of the board
        return "\n".join(
            [" | ".join([cell.value if cell else " " for cell in row]) for row in self.grid]
        )
