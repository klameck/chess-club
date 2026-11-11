from copy import deepcopy
#from move import Move
#from undo import UndoState
from dataclasses import dataclass
from typing import Iterable

WHITE = 0
BLACK = 1

PAWN = 0
KNIGHT = 1
BISHOP = 2
ROOK = 3
QUEEN = 4
KING = 5

PIECE_TYPES = 6
COLORS = 2

BOARD_SIZE = 64

FULL_MASK = (1 << BOARD_SIZE) - 1

NO_SQUARE = -1

STARTING_FEN = (
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/"
    "RNBQKBNR w KQkq - 0 1"
)

# Castling rights
WHITE_KINGSIDE = 1
WHITE_QUEENSIDE = 2
BLACK_KINGSIDE = 4
BLACK_QUEENSIDE = 8

ALL_CASTLING_RIGHTS = 15


# ============================================================
# CONSTANTS
# ============================================================

BOTH = 2

PROMOTION_PIECES = (QUEEN, ROOK, BISHOP, KNIGHT)

PIECE_TO_SYMBOL = {
    (WHITE, PAWN): "P",
    (WHITE, KNIGHT): "N",
    (WHITE, BISHOP): "B",
    (WHITE, ROOK): "R",
    (WHITE, QUEEN): "Q",
    (WHITE, KING): "K",
    (BLACK, PAWN): "p",
    (BLACK, KNIGHT): "n",
    (BLACK, BISHOP): "b",
    (BLACK, ROOK): "r",
    (BLACK, QUEEN): "q",
    (BLACK, KING): "k",
}

PROMOTION_SYMBOLS = {
    KNIGHT: "n",
    BISHOP: "b",
    ROOK: "r",
    QUEEN: "q",
}

BISHOP_DIRECTIONS = (
    (-1, -1), (-1, 1),
    (1, -1), (1, 1),
)

ROOK_DIRECTIONS = (
    (-1, 0), (1, 0),
    (0, -1), (0, 1),
)

KING_DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),            (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)

KNIGHT_DIRECTIONS = (
    (-2, -1), (-2, 1),
    (-1, -2), (-1, 2),
    (1, -2),  (1, 2),
    (2, -1),  (2, 1),
)


# ============================================================
# BITBOARD UTILITIES
# ============================================================

def set_bit(bitboard: int, square: int) -> int:
    return bitboard | (1 << square)


def clear_bit(bitboard: int, square: int) -> int:
    return bitboard & ~(1 << square) & FULL_MASK


def get_bit(bitboard: int, square: int) -> int:
    return (bitboard >> square) & 1


def pop_lsb(bitboard: int) -> tuple[int, int]:
    """Return the least significant set bit and remaining bitboard."""

    if bitboard == 0:
        raise ValueError("Cannot pop from an empty bitboard")

    square = (bitboard & -bitboard).bit_length() - 1
    bitboard &= bitboard - 1

    return square, bitboard


def iter_bits(bitboard: int):
    """Iterate over all occupied squares."""

    while bitboard:
        square, bitboard = pop_lsb(bitboard)
        yield square


def square_name(square: int) -> str:
    if not 0 <= square < 64:
        raise ValueError(f"Invalid square: {square}")

    file = square % 8
    rank = square // 8

    return chr(ord("a") + file) + str(rank + 1)


def parse_square(name: str) -> int:
    if (
        len(name) != 2
        or name[0] not in "abcdefgh"
        or name[1] not in "12345678"
    ):
        raise ValueError(f"Invalid square: {name}")

    file = ord(name[0]) - ord("a")
    rank = int(name[1]) - 1

    return rank * 8 + file


def get_rank(square: int) -> int:
    return square // 8


def get_file(square: int) -> int:
    return square % 8


# ============================================================
# MOVE REPRESENTATION
# ============================================================

@dataclass(frozen=True, slots=True)
class Move:
    from_square: int
    to_square: int
    promotion: int = -1

    def __str__(self) -> str:
        result = (
            square_name(self.from_square)
            + square_name(self.to_square)
        )

        if self.promotion != -1:
            result += PROMOTION_SYMBOLS[self.promotion]

        return result


# ============================================================
# UNDO STATE
# ============================================================

@dataclass(slots=True)
class UndoState:
    pieces: list[list[int]]
    side_to_move: int
    castling_rights: int
    en_passant_square: int
    halfmove_clock: int
    fullmove_number: int
    fen: str | None


# ============================================================
# BOARD
# ============================================================

class MagicBitBoard():

    def __init__(self, fen: str | None = None):

        super().__init__(fen)

        # 12 piece bitboards
        # pieces[color][piece_type]
        self.pieces = [
            [0] * PIECE_TYPES
            for _ in range(2)
        ]

        # White, black, both
        self.occupancies = [0, 0, 0]

        self.side_to_move = WHITE
        self.castling_rights = 0
        self.en_passant_square = NO_SQUARE

        self.halfmove_clock = 0
        self.fullmove_number = 1

        # Undo history
        self.history: list[UndoState] = []

        self.load_fen(fen or STARTING_FEN)

    # ========================================================
    # FEN PARSING
    # ========================================================

    def load_fen(self, fen: str) -> None:

        fields = fen.split()

        if len(fields) != 6:
            raise ValueError("FEN must contain exactly 6 fields")

        placement, active, castling, ep, halfmove, fullmove = fields

        self.pieces = [[0] * PIECE_TYPES for _ in range(2)]

        ranks = placement.split("/")

        if len(ranks) != 8:
            raise ValueError("FEN must contain exactly 8 ranks")

        for fen_rank, rank_data in enumerate(ranks):

            file = 0
            rank = 7 - fen_rank

            for char in rank_data:

                if char in "12345678":
                    file += int(char)

                elif char in PIECE_SYMBOLS:

                    if file >= 8:
                        raise ValueError("Too many squares in rank")

                    color, piece_type = PIECE_SYMBOLS[char]
                    square = rank * 8 + file

                    self.pieces[color][piece_type] |= 1 << square

                    file += 1

                else:
                    raise ValueError(f"Invalid FEN character: {char}")

                if file > 8:
                    raise ValueError("Too many squares in rank")

            if file != 8:
                raise ValueError(
                    f"Invalid number of squares in rank {8 - fen_rank}"
                )

        # Active color
        if active == "w":
            self.side_to_move = WHITE
        elif active == "b":
            self.side_to_move = BLACK
        else:
            raise ValueError("Invalid active color")

        # Castling rights
        self.castling_rights = 0

        if castling != "-":

            if any(c not in "KQkq" for c in castling):
                raise ValueError("Invalid castling rights")

            if len(set(castling)) != len(castling):
                raise ValueError("Duplicate castling rights")

            castling_map = {
                "K": WHITE_KINGSIDE,
                "Q": WHITE_QUEENSIDE,
                "k": BLACK_KINGSIDE,
                "q": BLACK_QUEENSIDE,
            }

            for char in castling:
                self.castling_rights |= castling_map[char]

        # En passant
        self.en_passant_square = (
            NO_SQUARE if ep == "-" else parse_square(ep)
        )

        if ep != "-":
            expected_rank = 5 if self.side_to_move == WHITE else 2

            if get_rank(self.en_passant_square) != expected_rank:
                raise ValueError("Invalid en passant rank")

        # Move counters
        try:
            self.halfmove_clock = int(halfmove)
            self.fullmove_number = int(fullmove)
        except ValueError as exc:
            raise ValueError("Invalid FEN move counters") from exc

        if self.halfmove_clock < 0 or self.fullmove_number < 1:
            raise ValueError("Invalid move counters")

        # Validate kings
        if self.pieces[WHITE][KING].bit_count() != 1:
            raise ValueError("Position must contain exactly one white king")

        if self.pieces[BLACK][KING].bit_count() != 1:
            raise ValueError("Position must contain exactly one black king")

        # Recalculate occupancy
        self.update_occupancies()

        self.fen = fen
        self.history.clear()

    # ========================================================
    # FEN GENERATION
    # ========================================================

    def to_fen(self) -> str:

        rows = []

        for rank in range(7, -1, -1):

            row = ""
            empty = 0

            for file in range(8):

                square = rank * 8 + file
                piece = self.piece_at(square)

                if piece is None:
                    empty += 1
                else:
                    if empty:
                        row += str(empty)
                        empty = 0

                    row += PIECE_TO_SYMBOL[piece]

            if empty:
                row += str(empty)

            rows.append(row)

        placement = "/".join(rows)

        active = "w" if self.side_to_move == WHITE else "b"

        castling = ""

        if self.castling_rights & WHITE_KINGSIDE:
            castling += "K"

        if self.castling_rights & WHITE_QUEENSIDE:
            castling += "Q"

        if self.castling_rights & BLACK_KINGSIDE:
            castling += "k"

        if self.castling_rights & BLACK_QUEENSIDE:
            castling += "q"

        if not castling:
            castling = "-"

        ep = (
            "-"
            if self.en_passant_square == NO_SQUARE
            else square_name(self.en_passant_square)
        )

        return (
            f"{placement} {active} {castling} {ep} "
            f"{self.halfmove_clock} {self.fullmove_number}"
        )

    # ========================================================
    # OCCUPANCY
    # ========================================================

    def update_occupancies(self) -> None:

        self.occupancies = [0, 0, 0]

        for piece_type in range(PIECE_TYPES):

            self.occupancies[WHITE] |= self.pieces[WHITE][piece_type]
            self.occupancies[BLACK] |= self.pieces[BLACK][piece_type]

        self.occupancies[BOTH] = (
            self.occupancies[WHITE] |
            self.occupancies[BLACK]
        )

    # ========================================================
    # PIECE ACCESS
    # ========================================================

    def piece_at(self, square: int):

        if not 0 <= square < 64:
            raise ValueError(f"Invalid square: {square}")

        bit = 1 << square

        for color in (WHITE, BLACK):

            for piece_type in range(PIECE_TYPES):

                if self.pieces[color][piece_type] & bit:
                    return color, piece_type

        return None

    def set_piece(
        self,
        color: int,
        piece_type: int,
        square: int
    ) -> None:

        if color not in (WHITE, BLACK):
            raise ValueError("Invalid color")

        if not 0 <= piece_type < PIECE_TYPES:
            raise ValueError("Invalid piece type")

        if not 0 <= square < 64:
            raise ValueError("Invalid square")

        if self.piece_at(square) is not None:
            raise ValueError(f"Square {square_name(square)} is occupied")

        self.pieces[color][piece_type] |= 1 << square

        self.update_occupancies()
        self.fen = None

    def remove_piece(self, square: int):

        piece = self.piece_at(square)

        if piece is None:
            raise ValueError(f"No piece on {square_name(square)}")

        color, piece_type = piece

        self.pieces[color][piece_type] &= ~(1 << square)

        self.update_occupancies()
        self.fen = None

        return piece

    # ========================================================
    # ATTACK GENERATION
    # ========================================================

    @staticmethod
    def knight_attacks(square: int) -> int:

        attacks = 0
        rank = get_rank(square)
        file = get_file(square)

        for dr, df in KNIGHT_DIRECTIONS:

            r = rank + dr
            f = file + df

            if 0 <= r < 8 and 0 <= f < 8:
                attacks |= 1 << (r * 8 + f)

        return attacks

    @staticmethod
    def king_attacks(square: int) -> int:

        attacks = 0
        rank = get_rank(square)
        file = get_file(square)

        for dr, df in KING_DIRECTIONS:

            r = rank + dr
            f = file + df

            if 0 <= r < 8 and 0 <= f < 8:
                attacks |= 1 << (r * 8 + f)

        return attacks

    @staticmethod
    def pawn_attacks(square: int, color: int) -> int:

        attacks = 0

        rank = get_rank(square)
        file = get_file(square)

        direction = 1 if color == WHITE else -1

        for df in (-1, 1):

            r = rank + direction
            f = file + df

            if 0 <= r < 8 and 0 <= f < 8:
                attacks |= 1 << (r * 8 + f)

        return attacks

    @staticmethod
    def sliding_attacks(
        square: int,
        occupancy: int,
        directions: tuple
    ) -> int:

        attacks = 0

        rank = get_rank(square)
        file = get_file(square)

        for dr, df in directions:

            r = rank + dr
            f = file + df

            while 0 <= r < 8 and 0 <= f < 8:

                target = r * 8 + f
                target_bit = 1 << target

                attacks |= target_bit

                # Stop after the first occupied square
                if occupancy & target_bit:
                    break

                r += dr
                f += df

        return attacks

    def bishop_attacks(self, square: int) -> int:

        return self.sliding_attacks(
            square,
            self.occupancies[BOTH],
            BISHOP_DIRECTIONS
        )

    def rook_attacks(self, square: int) -> int:

        return self.sliding_attacks(
            square,
            self.occupancies[BOTH],
            ROOK_DIRECTIONS
        )

    def queen_attacks(self, square: int) -> int:

        return (
            self.bishop_attacks(square) |
            self.rook_attacks(square)
        )

    # ========================================================
    # ATTACK DETECTION
    # ========================================================

    def is_square_attacked(
        self,
        square: int,
        by_color: int
    ) -> bool:

        # Pawn attacks
        pawns = self.pieces[by_color][PAWN]

        for pawn_square in iter_bits(pawns):

            if self.pawn_attacks(pawn_square, by_color) & (1 << square):
                return True

        # Knight attacks
        knights = self.pieces[by_color][KNIGHT]

        for knight_square in iter_bits(knights):

            if self.knight_attacks(knight_square) & (1 << square):
                return True

        # King attacks
        king = self.pieces[by_color][KING]

        if king:
            king_square = next(iter_bits(king))

            if self.king_attacks(king_square) & (1 << square):
                return True

        # Bishop and queen diagonal attacks
        diagonal = (
            self.pieces[by_color][BISHOP] |
            self.pieces[by_color][QUEEN]
        )

        for piece_square in iter_bits(diagonal):

            attacks = self.sliding_attacks(
                piece_square,
                self.occupancies[BOTH],
                BISHOP_DIRECTIONS
            )

            if attacks & (1 << square):
                return True

        # Rook and queen straight attacks
        straight = (
            self.pieces[by_color][ROOK] |
            self.pieces[by_color][QUEEN]
        )

        for piece_square in iter_bits(straight):

            attacks = self.sliding_attacks(
                piece_square,
                self.occupancies[BOTH],
                ROOK_DIRECTIONS
            )

            if attacks & (1 << square):
                return True

        return False

    def is_in_check(self, color: int) -> bool:

        king = self.pieces[color][KING]

        if king.bit_count() != 1:
            raise ValueError("Position must contain exactly one king")

        king_square = next(iter_bits(king))

        return self.is_square_attacked(
            king_square,
            1 - color
        )

    # ========================================================
    # PSEUDO-LEGAL MOVE GENERATION
    # ========================================================

    def generate_pseudo_legal_moves(self) -> list[Move]:

        moves = []

        color = self.side_to_move
        opponent = 1 - color

        friendly = self.occupancies[color]
        enemy = self.occupancies[opponent]

        enemy_king = self.pieces[opponent][KING]

        def add_move(from_sq, to_sq, promotion=-1):

            # Never generate a move that captures the enemy king
            if enemy_king & (1 << to_sq):
                return

            moves.append(Move(from_sq, to_sq, promotion))

        # ----------------------------------------------------
        # PAWNS
        # ----------------------------------------------------

        pawns = self.pieces[color][PAWN]

        direction = 8 if color == WHITE else -8
        start_rank = 1 if color == WHITE else 6
        promotion_rank = 7 if color == WHITE else 0

        for square in iter_bits(pawns):

            rank = get_rank(square)
            file = get_file(square)

            # One-square push
            one_step = square + direction

            if 0 <= one_step < 64:

                if not (self.occupancies[BOTH] & (1 << one_step)):

                    if get_rank(one_step) == promotion_rank:

                        for promotion in PROMOTION_PIECES:
                            add_move(square, one_step, promotion)

                    else:
                        add_move(square, one_step)

                        # Two-square push
                        two_step = square + 2 * direction

                        if rank == start_rank:
                            if not (
                                self.occupancies[BOTH] &
                                (1 << two_step)
                            ):
                                add_move(square, two_step)

            # Diagonal captures
            for df in (-1, 1):

                target_file = file + df

                if not 0 <= target_file < 8:
                    continue

                target = square + direction + df

                if not 0 <= target < 64:
                    continue

                target_bit = 1 << target

                # Normal capture
                if enemy & target_bit:

                    if get_rank(target) == promotion_rank:

                        for promotion in PROMOTION_PIECES:
                            add_move(square, target, promotion)

                    else:
                        add_move(square, target)

                # En passant
                elif target == self.en_passant_square:

                    captured_square = (
                        target - 8 if color == WHITE else target + 8
                    )

                    if (
                        self.pieces[opponent][PAWN] &
                        (1 << captured_square)
                    ):
                        add_move(square, target)

        # ----------------------------------------------------
        # KNIGHTS
        # ----------------------------------------------------

        knights = self.pieces[color][KNIGHT]

        for square in iter_bits(knights):

            attacks = self.knight_attacks(square)

            attacks &= ~friendly & FULL_MASK
            attacks &= ~enemy_king & FULL_MASK

            for target in iter_bits(attacks):
                add_move(square, target)

        # ----------------------------------------------------
        # BISHOPS
        # ----------------------------------------------------

        bishops = self.pieces[color][BISHOP]

        for square in iter_bits(bishops):

            attacks = self.bishop_attacks(square)

            attacks &= ~friendly & FULL_MASK
            attacks &= ~enemy_king & FULL_MASK

            for target in iter_bits(attacks):
                add_move(square, target)

        # ----------------------------------------------------
        # ROOKS
        # ----------------------------------------------------

        rooks = self.pieces[color][ROOK]

        for square in iter_bits(rooks):

            attacks = self.rook_attacks(square)

            attacks &= ~friendly & FULL_MASK
            attacks &= ~enemy_king & FULL_MASK

            for target in iter_bits(attacks):
                add_move(square, target)

        # ----------------------------------------------------
        # QUEENS
        # ----------------------------------------------------

        queens = self.pieces[color][QUEEN]

        for square in iter_bits(queens):

            attacks = self.queen_attacks(square)

            attacks &= ~friendly & FULL_MASK
            attacks &= ~enemy_king & FULL_MASK

            for target in iter_bits(attacks):
                add_move(square, target)

        # ----------------------------------------------------
        # KING
        # ----------------------------------------------------

        king = self.pieces[color][KING]
        king_square = next(iter_bits(king))

        attacks = self.king_attacks(king_square)

        attacks &= ~friendly & FULL_MASK
        attacks &= ~enemy_king & FULL_MASK

        for target in iter_bits(attacks):
            add_move(king_square, target)

        # ----------------------------------------------------
        # CASTLING
        # ----------------------------------------------------

        self.generate_castling_moves(moves)

        return moves

    # ========================================================
    # CASTLING GENERATION
    # ========================================================

    def generate_castling_moves(self, moves: list[Move]) -> None:

        color = self.side_to_move
        opponent = 1 - color

        if color == WHITE:

            king_square = 4
            rook_kingside = 7
            rook_queenside = 0

            kingside_right = WHITE_KINGSIDE
            queenside_right = WHITE_QUEENSIDE

            kingside_empty = (5, 6)
            queenside_empty = (1, 2, 3)

            kingside_transit = (5, 6)
            queenside_transit = (3, 2)

        else:

            king_square = 60
            rook_kingside = 63
            rook_queenside = 56

            kingside_right = BLACK_KINGSIDE
            queenside_right = BLACK_QUEENSIDE

            kingside_empty = (61, 62)
            queenside_empty = (57, 58, 59)

            kingside_transit = (61, 62)
            queenside_transit = (59, 58)

        # King must be on its original square
        if not (self.pieces[color][KING] & (1 << king_square)):
            return

        # Cannot castle while in check
        if self.is_square_attacked(king_square, opponent):
            return

        # Kingside castling
        if self.castling_rights & kingside_right:

            rook_exists = (
                self.pieces[color][ROOK] &
                (1 << rook_kingside)
            )

            empty = all(
                not (self.occupancies[BOTH] & (1 << sq))
                for sq in kingside_empty
            )

            safe = all(
                not self.is_square_attacked(sq, opponent)
                for sq in kingside_transit
            )

            if rook_exists and empty and safe:
                moves.append(
                    Move(king_square, king_square + 2)
                )

        # Queenside castling
        if self.castling_rights & queenside_right:

            rook_exists = (
                self.pieces[color][ROOK] &
                (1 << rook_queenside)
            )

            empty = all(
                not (self.occupancies[BOTH] & (1 << sq))
                for sq in queenside_empty
            )

            safe = all(
                not self.is_square_attacked(sq, opponent)
                for sq in queenside_transit
            )

            if rook_exists and empty and safe:
                moves.append(
                    Move(king_square, king_square - 2)
                )

    # ========================================================
    # LEGAL MOVE GENERATION
    # ========================================================

    def get_legal_moves(self) -> Iterable[Move]:

        legal_moves = []

        moving_color = self.side_to_move

        for move in self.generate_pseudo_legal_moves():

            self.push_move(move)

            legal = not self.is_in_check(moving_color)

            self.pop_move()

            if legal:
                legal_moves.append(move)

        return legal_moves

    # ========================================================
    # SAVE AND RESTORE STATE
    # ========================================================

    def save_state(self) -> UndoState:

        return UndoState(
            pieces=[row.copy() for row in self.pieces],
            side_to_move=self.side_to_move,
            castling_rights=self.castling_rights,
            en_passant_square=self.en_passant_square,
            halfmove_clock=self.halfmove_clock,
            fullmove_number=self.fullmove_number,
            fen=self.fen,
        )

    def restore_state(self, state: UndoState) -> None:

        self.pieces = [row.copy() for row in state.pieces]

        self.side_to_move = state.side_to_move
        self.castling_rights = state.castling_rights
        self.en_passant_square = state.en_passant_square

        self.halfmove_clock = state.halfmove_clock
        self.fullmove_number = state.fullmove_number

        self.fen = state.fen

        self.update_occupancies()

    # ========================================================
    # MAKE MOVE
    # ========================================================

    def push_move(self, move: any) -> None:

        if not isinstance(move, Move):
            raise TypeError("Expected a Move object")

        from_sq = move.from_square
        to_sq = move.to_square

        if (
            not 0 <= from_sq < 64
            or not 0 <= to_sq < 64
            or from_sq == to_sq
        ):
            raise ValueError("Invalid move squares")

        moving_piece = self.piece_at(from_sq)

        if moving_piece is None:
            raise ValueError("No piece on source square")

        color, piece_type = moving_piece
        opponent = 1 - color

        if color != self.side_to_move:
            raise ValueError("Moving the wrong color")

        destination_piece = self.piece_at(to_sq)

        if destination_piece is not None:
            if destination_piece[0] == color:
                raise ValueError("Cannot capture your own piece")

            if destination_piece[1] == KING:
                raise ValueError("Cannot capture the enemy king")

        # Identify special moves
        is_castling = (
            piece_type == KING and abs(to_sq - from_sq) == 2
        )

        is_en_passant = (
            piece_type == PAWN
            and to_sq == self.en_passant_square
            and destination_piece is None
            and get_file(from_sq) != get_file(to_sq)
        )

        is_capture = (
            destination_piece is not None or is_en_passant
        )

        # Validate en passant
        captured_square = to_sq

        if is_en_passant:

            captured_square = (
                to_sq - 8 if color == WHITE else to_sq + 8
            )

            if not (
                self.pieces[opponent][PAWN] &
                (1 << captured_square)
            ):
                raise ValueError("Invalid en passant capture")

        # Validate promotion
        last_rank = 7 if color == WHITE else 0

        if piece_type == PAWN and get_rank(to_sq) == last_rank:

            if move.promotion not in PROMOTION_PIECES:
                raise ValueError("Pawn reaching last rank must promote")

        elif move.promotion != -1:
            raise ValueError("Only pawns can promote")

        # Validate castling rook
        if is_castling:

            rook_from = from_sq + 3 if to_sq > from_sq else from_sq - 4

            if not (
                self.pieces[color][ROOK] &
                (1 << rook_from)
            ):
                raise ValueError("Castling rook is missing")

        # Save state only after basic validation
        self.history.append(self.save_state())

        # Remove captured piece
        if is_capture:

            self.pieces[opponent][
                PAWN if is_en_passant else destination_piece[1]
            ] &= ~(1 << captured_square)

        # Remove moving piece
        self.pieces[color][piece_type] &= ~(1 << from_sq)

        # Place moving piece or promoted piece
        if move.promotion != -1:
            self.pieces[color][move.promotion] |= 1 << to_sq
        else:
            self.pieces[color][piece_type] |= 1 << to_sq

        # Move rook during castling
        if is_castling:

            rook_to = from_sq + 1 if to_sq > from_sq else from_sq - 1

            self.pieces[color][ROOK] &= ~(1 << rook_from)
            self.pieces[color][ROOK] |= 1 << rook_to

        # Update castling rights after king movement
        if piece_type == KING:

            if color == WHITE:
                self.castling_rights &= ~(
                    WHITE_KINGSIDE | WHITE_QUEENSIDE
                )
            else:
                self.castling_rights &= ~(
                    BLACK_KINGSIDE | BLACK_QUEENSIDE
                )

        # Update rights when a rook moves
        rook_rights = {
            0: WHITE_QUEENSIDE,
            7: WHITE_KINGSIDE,
            56: BLACK_QUEENSIDE,
            63: BLACK_KINGSIDE,
        }

        if piece_type == ROOK:
            self.castling_rights &= ~rook_rights.get(from_sq, 0)

        # Update rights when a rook is captured
        if is_capture:
            self.castling_rights &= ~rook_rights.get(
                captured_square, 0
            )

        # Update en passant square
        self.en_passant_square = NO_SQUARE

        if piece_type == PAWN and abs(to_sq - from_sq) == 16:
            self.en_passant_square = (from_sq + to_sq) // 2

        # Update halfmove clock
        if piece_type == PAWN or is_capture:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # Update fullmove number
        if color == BLACK:
            self.fullmove_number += 1

        # Switch active player
        self.side_to_move = opponent

        self.update_occupancies()

        self.fen = None

    # ========================================================
    # UNMAKE MOVE
    # ========================================================

    def pop_move(self) -> None:

        if not self.history:
            raise ValueError("No moves to undo")

        previous_state = self.history.pop()

        self.restore_state(previous_state)

    # ========================================================
    # BOARD DISPLAY
    # ========================================================

    def print_board(self) -> None:

        print("  +---+---+---+---+---+---+---+---+")

        for rank in range(7, -1, -1):

            row = f"{rank + 1} |"

            for file in range(8):

                square = rank * 8 + file
                piece = self.piece_at(square)

                symbol = (
                    PIECE_TO_SYMBOL[piece]
                    if piece is not None
                    else " "
                )

                row += f" {symbol} |"

            print(row)
            print("  +---+---+---+---+---+---+---+---+")

        print("    a   b   c   d   e   f   g   h")

    def __str__(self) -> str:
        return self.to_fen()




board = MagicBitBoard()

# Print initial position
board.print_board()

# Generate legal moves
moves = list(board.get_legal_moves())

print("\nLegal moves:")
print([str(move) for move in moves])

print("\nNumber of legal moves:", len(moves))

assert len(moves) == 20

# Play e2-e4
move = Move(12, 28)

board.push_move(move)

print("\nAfter e2-e4:")
board.print_board()

print("FEN:", board.to_fen())

# Undo
board.pop_move()

print("\nAfter undo:")
board.print_board()

assert board.to_fen() == (
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/"
    "RNBQKBNR w KQkq - 0 1"
)

print("\nAll tests passed!")
