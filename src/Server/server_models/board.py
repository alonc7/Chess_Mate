from typing import List, Optional
from server_referee.king_rules import get_castling_moves, get_possible_king_moves
from server_referee.knight_rules import get_possible_knight_moves
from server_referee.queen_rules import get_possible_queen_moves
from server_referee.bishop_rules import get_possible_bishop_moves
from server_referee.rook_rules import get_possible_rook_moves
from server_referee.pawn_rules import get_possible_pawn_moves

from .piece import Piece
from .position import Position
from .pawn import Pawn
from server_types import types


class Board:
    def __init__(self, pieces: List[Piece], total_turns: int):
        self.pieces = pieces
        self.total_turns = total_turns
        self.winning_team: Optional[types.TeamType] = None

    @property
    def current_team(self) -> types.TeamType:
        return types.TeamType.OPPONENT if self.total_turns % 2 == 0 else types.TeamType.TEAMMATE

    def calculate_all_moves(self) -> None:
        for piece in self.pieces:
            piece.possible_moves = self.get_valid_moves(piece, self.pieces)

        for king in [p for p in self.pieces if p.is_king]:
            if king.possible_moves is None:
                continue
            king.possible_moves.extend(get_castling_moves(king, self.pieces))

        self.check_current_team_moves()

        for piece in [p for p in self.pieces if p.team != self.current_team]:
            piece.possible_moves = []

        if any(p for p in self.pieces if p.team == self.current_team and p.possible_moves):
            return

        self.winning_team = types.TeamType.OPPONENT if self.current_team == types.TeamType.TEAMMATE else types.TeamType.TEAMMATE

    def check_current_team_moves(self) -> None:
        for piece in [p for p in self.pieces if p.team == self.current_team]:
            if piece.possible_moves is None:
                continue

            for move in piece.possible_moves:
                simulated_board = self.clone()

                simulated_board.pieces = [
                    p for p in simulated_board.pieces if not p.same_position(move)]

                cloned_piece = next(
                    p for p in simulated_board.pieces if p.same_piece_position(piece))
                cloned_piece.position = move.clone()

                cloned_king = next(
                    p for p in simulated_board.pieces if p.is_king and p.team == simulated_board.current_team)

                for enemy in [p for p in simulated_board.pieces if p.team != simulated_board.current_team]:
                    enemy.possible_moves = simulated_board.get_valid_moves(
                        enemy, simulated_board.pieces)

                    if enemy.is_pawn:
                        if any(m for m in enemy.possible_moves if m.x != enemy.position.x and m.same_position(cloned_king.position)):
                            piece.possible_moves = [
                                m for m in piece.possible_moves if not m.same_position(move)]
                    else:
                        if any(m for m in enemy.possible_moves if m.same_position(cloned_king.position)):
                            piece.possible_moves = [
                                m for m in piece.possible_moves if not m.same_position(move)]

    def get_valid_moves(self, piece: Piece, board_state: List[Piece]) -> List[Position]:
        if piece.type == types.PieceType.PAWN:
            return get_possible_pawn_moves(piece, board_state)
        elif piece.type == types.PieceType.KNIGHT:
            return get_possible_knight_moves(piece, board_state)
        elif piece.type == types.PieceType.BISHOP:
            return get_possible_bishop_moves(piece, board_state)
        elif piece.type == types.PieceType.ROOK:
            return get_possible_rook_moves(piece, board_state)
        elif piece.type == types.PieceType.QUEEN:
            return get_possible_queen_moves(piece, board_state)
        elif piece.type == types.PieceType.KING:
            return get_possible_king_moves(piece, board_state)
        else:
            return []

    def play_move(self, en_passant_move: bool, valid_move: bool, played_piece: Piece, destination: Position) -> bool:
        pawn_direction = 1 if played_piece.team == types.TeamType.TEAMMATE else -1
        destination_piece = next(
            (p for p in self.pieces if p.same_position(destination)), None)

        if played_piece.is_king and destination_piece and destination_piece.is_rook and destination_piece.team == played_piece.team:
            direction = 1 if destination_piece.position.x - \
                played_piece.position.x > 0 else -1
            new_king_x_position = played_piece.position.x + direction * 2

            self.pieces = [
                p if not p.same_piece_position(
                    played_piece) else p.clone_with_new_position(x=new_king_x_position)
                for p in self.pieces
            ]

            self.calculate_all_moves()
            return True

        if en_passant_move:
            self.pieces = [
                p.clone_with_new_position(x=destination.x, y=destination.y) if p.same_piece_position(played_piece) and isinstance(p, Pawn) else
                p.clone_with_new_position(x=p.position.x, y=p.position.y) if not p.same_position(Position(destination.x, destination.y - pawn_direction)) and isinstance(p, Pawn) else
                p
                for p in self.pieces
            ]

            self.calculate_all_moves()
        elif valid_move:
            self.pieces = [
                p.clone_with_new_position(x=destination.x, y=destination.y) if p.same_piece_position(played_piece) and isinstance(p, Pawn) and abs(played_piece.position.y - destination.y) == 2 and played_piece.type == types.PieceType.PAWN else
                p.clone_with_new_position(x=destination.x, y=destination.y) if p.same_piece_position(played_piece) else
                p.clone_with_new_position(x=p.position.x, y=p.position.y) if not p.same_position(destination) and isinstance(p, Pawn) else
                p
                for p in self.pieces
            ]

            self.calculate_all_moves()
        else:
            return False

        return True

    def to_dict(self):
        return {
            "pieces": self.pieces,
            "totalTurns": self.totalTurns
        }

    def clone(self) -> 'Board':
        return Board([p.clone() for p in self.pieces], self.total_turns)
