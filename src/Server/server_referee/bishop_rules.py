from typing import List
from server_models.piece import Piece
from server_models.position import Position
from server_types.types import TeamType
from server_referee.general_logic import *


def is_bishop_move_valid(initial_position: Position, desired_position: Position, team: TeamType, board_state: List[Piece]) -> bool:
    print(f"Inside is_bishop_move_valid: ...")
    for i in range(1, 8):
        if desired_position.x > initial_position.x and desired_position.y > initial_position.y:
            passed_position = Position(
                initial_position.x+i, initial_position.y+i)

            if passed_position.same_position(desired_position):
                if tile_is_empty_or_occupied(passed_position, board_state, team):
                    return True
                else:
                    if tile_is_occupied(passed_position, board_state):
                        break

        if desired_position.x > initial_position.x and desired_position.y < initial_position.y:
            passed_position = Position(
                initial_position.x + i, initial_position.y - i)

            if passed_position.same_position(desired_position):
                if tile_is_empty_or_occupied(passed_position, board_state, team):
                    return True
                else:
                    if tile_is_occupied(passed_position, board_state):
                        break

                # Bottom left movement
        if desired_position.x < initial_position.x and desired_position.y < initial_position.y:
            passed_position = Position(
                initial_position.x - i, initial_position.y - i)

            # Check if the tile is the destination tile
            if passed_position.same_position(desired_position):
                # Dealing with destination tile
                if tile_is_empty_or_occupied(passed_position, board_state, team):
                    return True
            else:
                if tile_is_occupied(passed_position, board_state):
                    break

        # Top left movement
        if desired_position.x < initial_position.x and desired_position.y > initial_position.y:
            passed_position = Position(
                initial_position.x - i, initial_position.y + i)

            # Check if the tile is the destination tile
            if passed_position.same_position(desired_position):
                # Dealing with destination tile
                if tile_is_empty_or_occupied(passed_position, board_state, team):
                    return True
            else:
                if tile_is_occupied(passed_position, board_state):
                    break

    return False


def get_possible_bishop_moves(bishop: Piece, board_state: list):
    possible_moves = []

    # Upper right movement
    for i in range(1, 8):
        destination = Position(bishop.position.x + i, bishop.position.y + i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, bishop.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Bottom right movement
    for i in range(1, 8):
        destination = Position(bishop.position.x + i, bishop.position.y - i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, bishop.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Bottom left movement
    for i in range(1, 8):
        destination = Position(bishop.position.x - i, bishop.position.y - i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, bishop.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Top left movement
    for i in range(1, 8):
        destination = Position(bishop.position.x - i, bishop.position.y + i)

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, bishop.team):
            possible_moves.append(destination)
            break
        else:
            break

    return possible_moves
