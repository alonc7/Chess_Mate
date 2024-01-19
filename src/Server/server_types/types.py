from enum import Enum

class PieceType(Enum):
    PAWN = 'pawn'
    BISHOP = 'bishop'
    KNIGHT = 'knight'
    ROOK = 'rook'
    QUEEN = 'queen'
    KING = 'king'


class TeamType(Enum):
    OPPONENT = 'b'
    TEAMMATE = 'w'
