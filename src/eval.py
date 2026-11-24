import board 
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

def iter_bits(bitboard: int):
    """Iterate over all occupied squares."""

    while bitboard:
        square, bitboard = pop_lsb(bitboard)
        yield square

def evaluate(board):
    scores = [0,0] # assumes [WHITE, BLACK]
    for color in [WHITE, BLACK]:
        """ Using basic material evaluation """
        # material values after Turing
        # assumes [PAWN, KNIGHT, BISHOP, ROOK, QUEEN]
        mat_vals = [100, 300, 350, 500, 1000] 
        for piece_type in [PAWN, KNIGHT, BISHOP, ROOK, QUEEN]:
            for piece in iter_bits(board.pieces[color][piece_type]):
                scores[color] += mat_vals[piece_type]
    
    
    return scores[1] - scores[0]
    

