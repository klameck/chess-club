import board 

from config import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, POS_TABLES

EVAL_FACTOR = 2 # relational value between 

PIECE_VALUES = {
    PAWN: 100,
    KNIGHT: 300,
    BISHOP: 350,
    ROOK: 500,
    QUEEN: 1000,
    KING: 0  # can't be captured anyways
}


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

def evaluate2(state):

    score = 0

    if state.is_stalemate():
        return 0

    #penalty for checkmate
    if state.is_checkmate():
        return -10000 if state.side_to_move == "WHITE" else 10000

    for color in [WHITE, BLACK]:

        # positive for white and negative for black
        sign = 1 if color == WHITE else -1

        for piece_type in PIECE_VALUES:

            for square in board.iter_bits(state.pieces[color][piece_type]):

                # material
                material = PIECE_VALUES[piece_type]

                # position
                positional = POS_TABLES[color][piece_type][square]

                score += sign * (material + positional * EVAL_FACTOR)

    return score

if __name__ == "__main__":
    chessboard = board.MagicBitBoard()
    chessboard.remove_piece(53)
    print(chessboard)

    # Print initial position
    chessboard.print_board()
    print(evaluate2(chessboard))