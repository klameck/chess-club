import board 

from config import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, POS_TABLES

EVAL_FACTOR = 2 # relational value between 

def evaluate(chessboard):
    mat_scores = [0,0] # assumes [WHITE, BLACK]
    pos_scores = [0,0]
    for color in [WHITE, BLACK]:
        """ Using basic material evaluation """
        # material values after Turing
        # assumes [PAWN, KNIGHT, BISHOP, ROOK, QUEEN]
        mat_vals = [100, 300, 350, 500, 1000, 10000] 
        for piece_type in [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]:
            for piece in board.iter_bits(chessboard.pieces[color][piece_type]):
                mat_scores[color] += mat_vals[piece_type]

                """ Positional tables """
                pos_scores[color] += POS_TABLES[color][piece_type][piece]
    
    # combine scores
    cum_score = (mat_scores[0] - mat_scores[1]) + (pos_scores[0] - pos_scores[1]) * EVAL_FACTOR
    return cum_score
    

if __name__ == "__main__":
    chessboard = board.MagicBitBoard()
    chessboard.remove_piece(0)
    print(chessboard)

    # Print initial position
    chessboard.print_board()
    print(evaluate(chessboard))