from typing import List, Optional
from server_types.types import PieceType, TeamType
from server_models.piece import Piece
from server_models.position import Position


class Pawn(Piece):
    def __init__(self, position: Position, team: TeamType, has_moved: bool, en_passant: Optional[bool] = None, possible_moves: List[Position] = []):
        super().__init__(position, PieceType.PAWN, team, has_moved, possible_moves)
        self.en_passant = en_passant

    def clone(self) -> 'Pawn':
        return Pawn(self.position.clone(), self.team, self.has_moved, self.en_passant, [m.clone() for m in self.possible_moves])
