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


def evaluate(chessboard):
    scores = [0,0] # assumes [WHITE, BLACK]
    for color in [WHITE, BLACK]:
        """ Using basic material evaluation """
        # material values after Turing
        # assumes [PAWN, KNIGHT, BISHOP, ROOK, QUEEN]
        mat_vals = [100, 300, 350, 500, 1000] 
        for piece_type in [PAWN, KNIGHT, BISHOP, ROOK, QUEEN]:
            for piece in board.iter_bits(chessboard.pieces[color][piece_type]):
                scores[color] += mat_vals[piece_type]
    
    
    return scores[1] - scores[0]
    

if __name__ == "__main__":
    print("djf")
    chessboard = board.MagicBitBoard("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")

    # Print initial position
    chessboard.print_board()
    print(evaluate(chessboard))