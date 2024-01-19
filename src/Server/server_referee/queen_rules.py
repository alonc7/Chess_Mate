from server_types.types import TeamType
from server_models.piece import Piece
from server_models.position import Position
from server_referee.general_logic import tile_is_empty_or_occupied, tile_is_occupied
from typing import List


def is_queen_valid_move(initial_position: Position, desired_position: Position, team: TeamType, board_state: list) -> bool:
    for i in range(1, 8):
        # Diagonal
        multiplier_x = -1 if desired_position.x < initial_position.x else (
            1 if desired_position.x > initial_position.x else 0)
        multiplier_y = -1 if desired_position.y < initial_position.y else (
            1 if desired_position.y > initial_position.y else 0)

        passed_position = Position(
            initial_position.x + (i * multiplier_x), initial_position.y + (i * multiplier_y))

        if passed_position.same_position(desired_position):
            if tile_is_empty_or_occupied(passed_position, board_state, team):
                return True
        else:
            if tile_is_occupied(passed_position, board_state):
                break

    return False


def get_possible_queen_moves(queen: Piece, board_state: list) -> list:
    possible_moves = []

    # Top movement
    for i in range(1, 8):
        destination = Position(queen.position.x, queen.position.y + i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_empty_or_occupied(destination, board_state, queen.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Bottom movement
    for i in range(1, 8):
        destination = Position(queen.position.x, queen.position.y - i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_empty_or_occupied(destination, board_state, queen.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Left movement
    for i in range(1, 8):
        destination = Position(queen.position.x - i, queen.position.y)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_empty_or_occupied(destination, board_state, queen.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Right movement
    for i in range(1, 8):
        destination = Position(queen.position.x + i, queen.position.y)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_empty_or_occupied(destination, board_state, queen.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Upper right movement
    for i in range(1, 8):
        destination = Position(queen.position.x + i, queen.position.y + i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_empty_or_occupied(destination, board_state, queen.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Bottom right movement
    for i in range(1, 8):
        destination = Position(queen.position.x + i, queen.position.y - i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_empty_or_occupied(destination, board_state, queen.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Bottom left movement
    for i in range(1, 8):
        destination = Position(queen.position.x - i, queen.position.y - i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_empty_or_occupied(destination, board_state, queen.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Top left movement
    for i in range(1, 8):
        destination = Position(queen.position.x - i, queen.position.y + i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_empty_or_occupied(destination, board_state, queen.team):
            possible_moves.append(destination)
            break
        else:
            break

    return possible_moves
