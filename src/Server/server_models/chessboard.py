from typing import List
from server_models.board import Board
from server_models.pawn import Pawn
from server_models.piece import Piece
from server_models.position import Position
from server_types.types import PieceType, TeamType

VERTICAL_AXIS = ["1", "2", "3", "4", "5", "6", "7", "8"]
HORIZONTAL_AXIS = ["a", "b", "c", "d", "e", "f", "g", "h"]

GRID_SIZE = 100

initial_board = Board([
    Piece(Position(0, 7), PieceType.ROOK, TeamType.OPPONENT, False),
    Piece(Position(1, 7), PieceType.KNIGHT, TeamType.OPPONENT, False),
    Piece(Position(2, 7), PieceType.BISHOP, TeamType.OPPONENT, False),
    Piece(Position(3, 7), PieceType.QUEEN, TeamType.OPPONENT, False),
    Piece(Position(4, 7), PieceType.KING, TeamType.OPPONENT, False),
    Piece(Position(5, 7), PieceType.BISHOP, TeamType.OPPONENT, False),
    Piece(Position(6, 7), PieceType.KNIGHT, TeamType.OPPONENT, False),
    Piece(Position(7, 7), PieceType.ROOK, TeamType.OPPONENT, False),
    Pawn(Position(0, 6), TeamType.OPPONENT, False),
    Pawn(Position(1, 6), TeamType.OPPONENT, False),
    Pawn(Position(2, 6), TeamType.OPPONENT, False),
    Pawn(Position(3, 6), TeamType.OPPONENT, False),
    Pawn(Position(4, 6), TeamType.OPPONENT, False),
    Pawn(Position(5, 6), TeamType.OPPONENT, False),
    Pawn(Position(6, 6), TeamType.OPPONENT, False),
    Pawn(Position(7, 6), TeamType.OPPONENT, False),
    Piece(Position(0, 0), PieceType.ROOK, TeamType.TEAMMATE, False),
    Piece(Position(1, 0), PieceType.KNIGHT, TeamType.TEAMMATE, False),
    Piece(Position(2, 0), PieceType.BISHOP, TeamType.TEAMMATE, False),
    Piece(Position(3, 0), PieceType.QUEEN, TeamType.TEAMMATE, False),
    Piece(Position(4, 0), PieceType.KING, TeamType.TEAMMATE, False),
    Piece(Position(5, 0), PieceType.BISHOP, TeamType.TEAMMATE, False),
    Piece(Position(6, 0), PieceType.KNIGHT, TeamType.TEAMMATE, False),
    Piece(Position(7, 0), PieceType.ROOK, TeamType.TEAMMATE, False),
    Pawn(Position(0, 1), TeamType.TEAMMATE, False),
    Pawn(Position(1, 1), TeamType.TEAMMATE, False),
    Pawn(Position(2, 1), TeamType.TEAMMATE, False),
    Pawn(Position(3, 1), TeamType.TEAMMATE, False),
    Pawn(Position(4, 1), TeamType.TEAMMATE, False),
    Pawn(Position(5, 1), TeamType.TEAMMATE, False),
    Pawn(Position(6, 1), TeamType.TEAMMATE, False),
    Pawn(Position(7, 1), TeamType.TEAMMATE, False),
], 1)

initial_board.calculate_all_moves()
