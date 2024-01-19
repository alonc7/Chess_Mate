from server_types.types import TeamType
from typing import Union, List
from server_models.piece import Piece
from server_models.position import Position
from server_referee.general_logic import tile_is_occupied, tile_is_occupied_by_opponent


from server_referee.general_logic import tile_is_occupied, tile_is_occupied_by_opponent


def is_pawn_valid_move(new_position: Position, initial_position: Position, team: Union[str, TeamType], board_state: List[Piece]) -> bool:
    team = TeamType(team) if isinstance(team, str) else team
    special_row = 1 if team == TeamType.TEAMMATE else 6
    pawn_direction = 1 if team == TeamType.TEAMMATE else -1
    special_position_move = Position(
        new_position.x, new_position.y - pawn_direction)
 
    # Movement Logic
    if new_position.x == initial_position.x and new_position.y == initial_position.y:
        print("Invalid move: Same position.")
        return False

    if (
        initial_position.x == new_position.x
        and initial_position.y == special_row
        and new_position.y - initial_position.y == 2 * pawn_direction
    ):

        if (
            not tile_is_occupied(new_position, board_state)
            and not tile_is_occupied(special_position_move, board_state)
        ):
            return True

    elif (
        initial_position.x == new_position.x
        and new_position.y - initial_position.y == pawn_direction
    ):
        if not tile_is_occupied(new_position, board_state):
            print("Valid move: Single move.")
            return True

    # Attack Logic for the pawn
    elif (
        new_position.x - initial_position.x == -1
        and new_position.y - initial_position.y == pawn_direction
    ):
        if tile_is_occupied_by_opponent(new_position, board_state, team):
            print("Valid move: Attack to the left.")
            return True

    elif (
        new_position.x - initial_position.x == 1
        and new_position.y - initial_position.y == pawn_direction
    ):
        if tile_is_occupied_by_opponent(new_position, board_state, team):
            print("Valid move: Attack to the right.")
            return True

    print("Invalid move.")
    return False


def get_possible_pawn_moves(pawn: Piece, board_state: list) -> list:
    possible_moves = []
    special_row = 1 if pawn.team == TeamType.TEAMMATE else 6
    pawn_direction = 1 if pawn.team == TeamType.TEAMMATE else -1

    normal_move = Position(pawn.position.x, pawn.position.y + pawn_direction)
    special_move = Position(normal_move.x, normal_move.y + pawn_direction)
    upper_left_attack = Position(
        pawn.position.x - 1, pawn.position.y + pawn_direction)
    upper_right_attack = Position(
        pawn.position.x + 1, pawn.position.y + pawn_direction)
    left_position = Position(pawn.position.x - 1, pawn.position.y)
    right_position = Position(pawn.position.x + 1, pawn.position.y)

    if not tile_is_occupied(normal_move, board_state):
        possible_moves.append(normal_move)

        if not tile_is_occupied(special_move, board_state) and pawn.position.y == special_row:
            possible_moves.append(special_move)

    left_piece = return_enPassant_piece(board_state, left_position)
    if left_piece and left_piece.en_passant:
        possible_moves.append(upper_left_attack)

    right_piece = return_enPassant_piece(board_state, right_position)
    if right_piece and right_piece.en_passant:
        possible_moves.append(upper_right_attack)

    return possible_moves


def return_enPassant_piece(board_state: List[Piece], checked_position: Position) -> Piece:
    for piece in board_state:
        if isinstance(piece, Piece):
            if piece.position.same_position(checked_position):
                return piece
    return None
