from typing import List
from server_types.types import TeamType, PieceType
from server_models.position import Position
class Piece:
    def __init__(self, position: Position, type: PieceType, team: TeamType, has_moved: bool, possible_moves: List[Position] = []):
        self.image = f'assets/images/{type.value}_{team.value}.png'
        self.position = position
        self.type = type
        self.team = team
        self.possible_moves = possible_moves
        self.has_moved = has_moved

    @property
    def is_pawn(self) -> bool:
        return self.type == PieceType.PAWN

    @property
    def is_rook(self) -> bool:
        return self.type == PieceType.ROOK

    @property
    def is_knight(self) -> bool:
        return self.type == PieceType.KNIGHT

    @property
    def is_bishop(self) -> bool:
        return self.type == PieceType.BISHOP

    @property
    def is_king(self) -> bool:
        return self.type == PieceType.KING

    @property
    def is_queen(self) -> bool:
        return self.type == PieceType.QUEEN

    def same_piece_position(self, other_piece: 'Piece') -> bool:
        return self.position.same_position(other_piece.position)

    def same_position(self, other_position: Position) -> bool:
        return self.position.same_position(other_position)
    def clone(self) -> 'Piece':
        return Piece(self.position.clone(), self.type, self.team, self.has_moved, [m.clone() for m in self.possible_moves])
