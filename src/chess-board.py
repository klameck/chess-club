"""
The board should mimic the basic interface of a python-chess board. 
Provide: - legal_moves - is_check - is_checkmate
"""

"""
BOARD REPRESENTATION
0    1  2  3  4  5  6  7  8    9
10   11 12 13 14 15 16 17 18   19
    -------------------------
20 | r  n  b  q  k  b  n  r  | 29
30 | p  p  p  p  p  p  p  p  | 39
40 | 41 42 43 44 45 46 47 48 | 49
50 | 51 52 53 54 55 56 57 58 | 59
60 | 61 62 63 64 65 66 67 68 | 69
70 | 71 72 73 74 75 76 77 78 | 79
80 | P  P  P  P  P  P  P  P  | 89 
90 | r  n  b  q  k  b  n  r  | 99
    -------------------------
100 101 102 103 104 105 106 107 108 109
110 111 112 113 114 115 116 117 118 119
"""

import math

PIECES = {
    0: "P",  # white pawn
    1: "N",  # white knight
    2: "B",  # white bishop
    3: "R",  # white rook
    4: "Q",  # white Queen
    5: "K",  # white King
    6: "p",  # black pawn
    7: "n",  # black knight
    8: "b",  # black bishop
    9: "r",  # black rook
    10: "q", # black Queen
    11: "k", # black King
}


EMPTY = None
BORDER = -1 

class ChessBoard():
    """Standard 8x8 board in a 10x12 mailbox (120 repuares, index = row*12 + col).
    Off-board repuares are OFF (-1), so edge moves need no bounds checks."""
    

    def __init__(self):
        self.pieces = [[x for x in range(81, 89)], # white pawns
                    [92, 97],   # white knigt
                    [93, 96],   # white bishop
                    [91, 98],   # white rook
                    [94],       # white queen
                    [95],       # white king    
                    [x for x in range(31, 39)], # black pawns
                    [22, 17],   # black knigt
                    [13, 16],   # black bishop
                    [21, 28],   # black rook
                    [24],       # black queen
                    [25]        # black king
                        ]
        # all moves will be saved here
        self.history = []
        self.player_white = True 

        self.sq = [EMPTY] * 120

        border_indices = (
            set(range(0, 20))
            | set(range(100, 120))
            | {i for i in range(20, 100) if i % 10 in (0, 9)}
        )

        for i in border_indices:
            self.sq[i] = BORDER 

        # standard set up
        for i, pc in enumerate([3, 1, 2, 4, 5, 2, 1, 3]):
            self.sq[21 + i] = pc            # rank 8 (row 1)
            self.sq[31 + i] = 1           # rank 7 (row 2)
            self.sq[81 + i] = 6           # rank 2 (row 7)
            self.sq[91 + i] = pc + 6    # rank 1 (row 8)

        
        
        
        # purely for looking at it / checking stuff at this point!
        self.rep = list(range(0, 120))

        # standard set up
        for i, pc in enumerate("rnbqkbnr"):
            self.rep[21 + i] = pc            # rank 8 (row 1)
            self.rep[31 + i] = "p"           # rank 7 (row 2)
            self.rep[81 + i] = "P"           # rank 2 (row 7)
            self.rep[91 + i] = pc.upper()    # rank 1 (row 8)


    def __str__(self):
        return "\n".join(
            " ".join(f"{self.sq[rank*10 + file]}" 
            for file in range(0, 10)) 
            for rank in range(0, 12)
        ) + "\n\n"

    def representation(self):
        return "\n".join(
            " ".join(f"{self.rep[rank*10 + file]}" 
            for file in range(0, 10)) 
            for rank in range(0, 12)
        ) + "\n\n"

    def backstabbing(cur_sq, target_sq):
        if sq[target_sq] * sq[cur_sq] > 0:
            return "Illegal move, don't stab your own piece in the back!"



    def legal_moves():
        """ Returns list of all possible moves of one colour in UCI format"""
        # check for same colour piece on target square
        # this requires empty places to be 0 
        # and the colours to have opposing signs
        
         """   
        # piece 
        piece = 

        # rook
        if abs(piece) == 4:
            # files
            if dif % 10 = 0:
                # check for collisions on the way
                for i in range(1, dif):
                    # in file
                    if self.sq[cur_sq + i*10] != EMPTY:
                        return False
                
                # check if out of bounds ?

            # ranks
            elif math.floor( cur_sq / 10 ) == math.floor( target_sq / 10):
                # check for collisions on the way
                for i in range(1, dif):
                    if self.sq[cur_sq + i] != EMPTY:
                        return False

                # check if out of bounds ?
            else:
                return False

        
        # knight
        if abs(piece) == 2:
            if abs(dif) == 21 or abs(dif) == 19:
                # not needed to check for pieces in the way
                # check for out of bounds  
            
        else:
            return "Illegal move, you can't move like that..."

        pass"""


    def is_check():
        pass

    def is_checkmate():
        pass

if __name__ == "__main__":
    board = ChessBoard()
    print(board.__str__())
    print(board.representation())