class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def same_position(self, other_position: 'Position') -> bool:
        return self.x == other_position.x and self.y == other_position.y

    def __str__(self):
        return f"{{'x': {self.x}, 'y': {self.y}}}"

    def clone(self) -> 'Position':
        return Position(self.x, self.y)

    def to_dict(self):
        return {'x': self.x, 'y': self.y}
