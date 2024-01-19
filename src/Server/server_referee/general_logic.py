from typing import List
from server_types.types import TeamType
from server_models.piece import Piece
from server_models.position import Position


# def tile_is_occupied(position: Position, board_state: List[Piece]) -> bool:
#     return any(piece.same_position(position) for piece in board_state)
def tile_is_occupied(position: Position, board_state: List[Piece]) -> bool:
    piece = next((p for p in board_state if isinstance(p, Piece) and p.same_position(position)), None)
    return bool(piece)


def tile_is_occupied_by_opponent(position: Position, board_state: List[Piece], team: TeamType) -> bool:
    piece = next((p for p in board_state if p.same_position(
        position) and p.team != team), None)
    return bool(piece)


def tile_is_empty_or_occupied(position: Position, board_state: List[Piece], team: TeamType) -> bool:
    return not tile_is_occupied(position, board_state) or tile_is_occupied_by_opponent(position, board_state, team)
