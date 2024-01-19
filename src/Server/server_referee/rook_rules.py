from server_types.types import TeamType
from server_models.piece import Piece
from server_models.position import Position
from server_referee.general_logic import *
from typing import List


def is_rook_valid_move(new_position, initial_position, team, board_state):
    # BASIC MOVEMENT LOGIC FOR ROOK
    if not ((initial_position.x == new_position.x and initial_position.y != new_position.y) or
            (initial_position.x != new_position.x and initial_position.y == new_position.y)):
        return False

    delta_x = (new_position.x - initial_position.x) // abs(new_position.x -
                                                           initial_position.x) if new_position.x != initial_position.x else 0

    delta_y = (new_position.y - initial_position.y) // abs(new_position.y -
                                                           initial_position.y) if new_position.y != initial_position.y else 0

    current_position = Position(initial_position.x, initial_position.y)

    while (new_position.x != current_position.x and new_position.y == initial_position.y) or \
            (new_position.x == current_position.x and new_position.y != current_position.y):
        current_position.x += delta_x
        current_position.y += delta_y

        if tile_is_occupied(current_position, board_state):
            if tile_is_occupied_by_opponent(current_position, board_state, team):
                if current_position.x != new_position.x or current_position.y != new_position.y:
                    return False
                return True  # Valid move: Capture opponent's piece
            else:
                return False  # Invalid move: Tile is occupied by a teammate

    return True


def get_possible_rook_moves(rook, board_state):
    possible_moves = []

    def check_and_push_move(x_offset, y_offset):
        for index in range(1, 9):
            destination = Position(
                rook.position.x + index * x_offset, rook.position.y + index * y_offset)

            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination)
            elif tile_is_occupied_by_opponent(destination, board_state, rook.team):
                possible_moves.append(destination)
                # Break if an opponent's piece is encountered (capture possible)
                break
            else:
                # Break if the destination is occupied by a teammate (cannot move past own pieces)
                break

    check_and_push_move(0, -1)  # Move up
    check_and_push_move(0, 1)   # Move down
    check_and_push_move(1, 0)   # Move right
    check_and_push_move(-1, 0)  # Move left

    return possible_moves
