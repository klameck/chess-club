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

    """def backstabbing(cur_sq, target_sq):
        if board.sq[target_sq] * board.sq[cur_sq] > 0:
            return "Illegal move, don't stab your own piece in the back!"
            """



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

    def square_attacked(self, my_sqr, player_white):
        
        knight_offsets = [-21, -19, -12, -8, 8, 12, 19, 21]
        king_offset = [-10, 10, -1, 1, -11, -9, 9, 11]
        orth_offset = [10, -10, 1, -1]
        diag_offset = [-11, -9, 9, 11]

        #whites turn
        if player_white:
            pawn_offset = [9,11]
            orth_attackers = [3,4] #black rook and queen
            knight_attacker = 1 #black knight
            diag_attackers = [2,4] #black bishop and queen
            pawn_attacker = 0 #black pawn
            king_attacker = 5 #black king
            
        #blacks turn
        else:
            pawn_offset = [-9,-11] 
            orth_attackers = [9,10] #white rook and queen
            knight_attacker = 7 #white knight
            diag_attackers = [8,10] #white bishop and queen
            pawn_attacker = 6 #white pawn
            king_attacker = 11 #white king
            

        #check knight moves
        for offset in knight_offsets:
            if self.sq[my_sqr + offset] == knight_attacker: 
                return True
            
        #check for orthogonal attacks
        for offset in orth_offset:
            current_idx = my_sqr + offset
            while self.sq[current_idx] != -1: # until hitting boundary
                if self.sq[current_idx] != None: #if non-empty square
                    if self.sq[current_idx] in orth_attackers : # rook or queen
                        return True
                    break # Blocked by another piece
                current_idx += offset
        #check for diagonal attacks
        for offset in diag_offset:
            current_idx = my_sqr + offset
            while self.sq[current_idx] != -1: # until hitting boundary
                if self.sq[current_idx] != None: #if non-empty square
                    if self.sq[current_idx] in diag_attackers : # bishop or queen
                        return True
                    break # Blocked by another piece
                current_idx += offset

        #check pawn attacks 
        for offset in pawn_offset:
            current_idx = my_sqr + offset
            if self.sq[current_idx] == pawn_attacker: # pawn
                return True
        #check for king attack
        for offset in king_offset:
            current_idx = my_sqr + offset
            if self.sq[current_idx] == king_attacker: # king
                return True        
                
        return False
            
    def is_check(self):
        if self.player_white:
            king_loc = self.pieces[5][0]
            return board.square_attacked(king_loc, self.player_white)
        else:
            king_loc = self.pieces[11][0]
            return board.square_attacked(king_loc, self.player_white)

    def is_checkmate(self):
        return self.is_check() and len(self.legal_moves()) == 0  #is in chack and no legal moves left

if __name__ == "__main__":
    board = ChessBoard()
    print(board.__str__())
    print(board.representation())
