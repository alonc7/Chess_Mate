from server_types.types import TeamType
from server_models.piece import Piece
from server_models.position import Position
from server_referee.general_logic import *


def is_king_valid_move(
        initial_position: Position, desired_position: Position, team: TeamType, board_state: List[Piece]) -> bool:

    for i in range(1, 2):
        # Diagonal
        multiplier_x = -1 if desired_position.x < initial_position.x else 1 if desired_position.x > initial_position.x else 0
        multiplier_y = -1 if desired_position.y < initial_position.y else 1 if desired_position.y > initial_position.y else 0

        passed_position = Position(
            initial_position.x + (i * multiplier_x), initial_position.y + (i * multiplier_y))

        if passed_position.same_position(desired_position):
            if tile_is_occupied_by_opponent(passed_position, board_state, team):
                return True
        else:
            if tile_is_occupied(passed_position, board_state):
                break
    return False
    # Could also be weritten like this:
    # if passed_position.same_position(desired_position):
    #     if tile_is_occupied_by_opponent(passed_position, board_state, team):
    #         return True
    # else:
    #     return tile_is_occupied(passed_position, board_state)


def get_possible_king_moves(king: Piece, board_state: list) -> list:
    possible_moves = []

    for i in range(1, 2):
        # Top movement
        destination = Position(king.position.x, king.position.y + i)

        if 0 <= destination.x <= 7 and 0 <= destination.y <= 7:
            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination)
            elif tile_is_occupied_by_opponent(destination, board_state, king.team):
                possible_moves.append(destination)
                break
            else:
                break

        # Bottom movement
        destination = Position(king.position.x, king.position.y - i)

        if 0 <= destination.x <= 7 and 0 <= destination.y <= 7:
            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination)
            elif tile_is_occupied_by_opponent(destination, board_state, king.team):
                possible_moves.append(destination)
                break
            else:
                break

        # Left movement
        destination = Position(king.position.x - i, king.position.y)

        if 0 <= destination.x <= 7 and 0 <= destination.y <= 7:
            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination)
            elif tile_is_occupied_by_opponent(destination, board_state, king.team):
                possible_moves.append(destination)
                break
            else:
                break

        # Right movement
        destination = Position(king.position.x + i, king.position.y)

        if 0 <= destination.x <= 7 and 0 <= destination.y <= 7:
            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination)
            elif tile_is_occupied_by_opponent(destination, board_state, king.team):
                possible_moves.append(destination)
                break
            else:
                break

        # Upper right movement
        destination = Position(king.position.x + i, king.position.y + i)

        if 0 <= destination.x <= 7 and 0 <= destination.y <= 7:
            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination)
            elif tile_is_occupied_by_opponent(destination, board_state, king.team):
                possible_moves.append(destination)
                break
            else:
                break

        # Bottom right movement
        destination = Position(king.position.x + i, king.position.y - i)

        if 0 <= destination.x <= 7 and 0 <= destination.y <= 7:
            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination)
            elif tile_is_occupied_by_opponent(destination, board_state, king.team):
                possible_moves.append(destination)
                break
            else:
                break

        # Bottom left movement
        destination = Position(king.position.x - i, king.position.y - i)

        if 0 <= destination.x <= 7 and 0 <= destination.y <= 7:
            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination)
            elif tile_is_occupied_by_opponent(destination, board_state, king.team):
                possible_moves.append(destination)
                break
            else:
                break

        # Top left movement
        destination = Position(king.position.x - i, king.position.y + i)

        if 0 <= destination.x <= 7 and 0 <= destination.y <= 7:
            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination)
            elif tile_is_occupied_by_opponent(destination, board_state, king.team):
                possible_moves.append(destination)
                break
            else:
                break

    return possible_moves


def get_castling_moves(king: Piece, board_state: list) -> list:
    possible_moves = []

    if king.has_moved:
        return possible_moves

    # Get the rooks from the king's team which haven't moved
    rooks = [p for p in board_state if p.is_rook and p.team ==
             king.team and not p.has_moved]

    # Loop through the rooks
    for rook in rooks:
        # Determine if we need to go to the right or the left side
        direction = 1 if rook.position.x - king.position.x > 0 else -1

        adjacent_position = king.position.clone()
        adjacent_position.x += direction

        if rook.possible_moves and adjacent_position in rook.possible_moves:
            # The rook can move to the adjacent side of the king
            concerning_tiles = [
                t for t in rook.possible_moves if t.y == king.position.y]

            # Checking if any of the enemy pieces can attack the spaces between
            # The rook and the king
            enemy_pieces = [p for p in board_state if p.team != king.team]

            valid = True

            for enemy in enemy_pieces:
                if enemy.possible_moves is None:
                    continue

                for move in enemy.possible_moves:
                    if move in concerning_tiles:
                        valid = False

                    if not valid:
                        break

                if not valid:
                    break

            if not valid:
                continue

            # Add it as a possible move
            possible_moves.append(rook.position.clone())

    return possible_moves
