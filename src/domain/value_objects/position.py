from src.domain.exceptions import InvalidMove

class Position:
    def __init__(self, x: int, y: int):
        if not (1 <= x <= 3 and 1 <= y <= 3):
            raise InvalidMove(f"Position {x},{y} out of board range (1-3)")
        self.x = x
        self.y = y

    @property
    def zero_indexed(self):
        return self.x - 1, self.y - 1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
