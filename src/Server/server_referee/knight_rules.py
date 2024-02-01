from server_models.position import Position
from server_referee.general_logic import tile_is_occupied, tile_is_occupied_by_opponent


def is_knight_valid_move(new_position, initial_position, team, board_state):
    delta_x = abs(new_position.x - initial_position.x)
    delta_y = abs(new_position.y - initial_position.y)

    new_position_move = Position(new_position.x, new_position.y)

    if (delta_x == 1 and delta_y == 2) or (delta_x == 2 and delta_y == 1):
        if not tile_is_occupied(new_position_move, board_state):
            return True
        elif tile_is_occupied_by_opponent(new_position_move, board_state, team):
            return True

    return False


def get_possible_knight_moves(knight, board_state):
    possible_moves = []

    for i in [-1, 1]:
        for j in [-1, 1]:
            horizontal_move = Position(
                knight.position.x + j, knight.position.y + i * 2)
            vertical_move = Position(
                knight.position.x + i * 2, knight.position.y + j)

            if not tile_is_occupied(vertical_move, board_state) or tile_is_occupied_by_opponent(vertical_move, board_state, knight.team):
                possible_moves.append(vertical_move)

            if not tile_is_occupied(horizontal_move, board_state) or tile_is_occupied_by_opponent(horizontal_move, board_state, knight.team):
                possible_moves.append(horizontal_move)

    return possible_moves
