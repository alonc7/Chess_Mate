from typing import List
from server_types.types import TeamType
from server_models.piece import Piece
from server_models.pawn import Pawn
from server_models.position import Position


# def tile_is_occupied(position: Position, board_state: List[Piece]) -> bool:
#     return any(piece.same_position(position) for piece in board_state)
def tile_is_occupied(position: Position, board_state: List[Piece]) -> bool:
    piece = next((p for p in board_state if isinstance(
        p, Piece) and p.same_position(position)), None)
    return bool(piece)


def tile_is_occupied_by_opponent(position: Position, board_state: List[Piece], team: TeamType) -> bool:
    return any(piece.position == position and piece.team != team for piece in board_state)


def tile_is_occupied_by_opponent2(new_position: Position, initial_position: Position, board_state: dict, team: str) -> bool:
    pawn_direction = 1 if team == 'w' else -1

    if (
        (new_position.x - initial_position.x == 1 and new_position.y - initial_position.y == pawn_direction) or
        (new_position.x - initial_position.x == -
         1 and new_position.y - initial_position.y == pawn_direction)
    ):
        for piece in board_state["pieces"]:
            opponent_condition = (
                # Check if it's the opponent's piece
                str(piece['team']) != team and
                str(piece['position']) == str(new_position)
            )
            if opponent_condition:
                print("Valid move: Attack.")
                return True

    return False


def tile_is_empty_or_occupied(position: Position, board_state: List[Piece], team: TeamType) -> bool:
    return not tile_is_occupied(position, board_state) or tile_is_occupied_by_opponent(position, board_state, team)
