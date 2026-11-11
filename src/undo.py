
from dataclasses import dataclass

@dataclass(slots=True)
class UndoState:
    pieces: list[list[int]]
    side_to_move: int
    castling_rights: int
    en_passant_square: int
    halfmove_clock: int
    fullmove_number: int
    fen: str | None
