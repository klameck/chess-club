"""
The board should mimic the basic interface of a python-chess board. 
Provide: - legal_moves - is_check - is_checkmate
"""

"""
TO DO
- en passant
- castelling
- draw rules
- promotion currently defaults queen
"""

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
        self.sq = [EMPTY] * 120
        border_indices = (
            set(range(0, 20))
            | set(range(100, 120))
            | {i for i in range(20, 100) if i % 10 in (0, 9)}
        )
        for i in border_indices:
                    self.sq[i] = BORDER 

        self.pieces = [[x for x in range(81, 89)], # white pawns
                    [92, 97],   # white knigts
                    [93, 96],   # white bishops
                    [91, 98],   # white rooks
                    [94],       # white queen
                    [95],       # white king    
                    [x for x in range(31, 39)], # black pawns
                    [22, 27],   # black knigts
                    [23, 26],   # black bishops
                    [21, 28],   # black rooks
                    [24],       # black queen
                    [25]        # black king
                        ]
        # all moves will be saved here
        self.history = []
        # white starts
        self.player_white = True 

        # standard set up
        for i, pc in enumerate([3, 1, 2, 4, 5, 2, 1, 3]):
            self.sq[21 + i] = pc + 6      # rank 8 (row 1)
            self.sq[31 + i] = 6           # rank 7 (row 2)
            self.sq[81 + i] = 0           # rank 2 (row 7)
            self.sq[91 + i] = pc          # rank 1 (row 8)
        
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
        """Return a readable board."""
        display = list(self.rep)
        for square in range(120):
            piece = self.sq[square]
            if piece is EMPTY:
                display[square] = "."
            elif piece == BORDER:
                display[square] = "#"
            else:
                display[square] = PIECES[piece]

        return "\n".join(
            " ".join(str(display[row * 10 + file]) for file in range(10))
            for row in range(12)
        )

    def steppable(self, target_sq):
        """ Checking if your own piece is on the target square or reaching a border.
        
            Return True if the square is empty or occupied by the other side.
            Return False if the square is occupied by your own piece.
            Return False if the square is actually out of bounds. """
        
        if self.sq[target_sq] == EMPTY:
            return True
        if self.sq[target_sq] == BORDER:
            return False

        #allow capturing enemy piece
        if self.player_white:
            return self.sq[target_sq] >= 6
        else:
            return self.sq[target_sq] < 6
                
            
    def coord(self, sq):
        file = sq % 10 -1
        rank = 10 - sq // 10 
        return f"{chr(ord('a') + file)}{rank}"

    def convert_to_uci(self, cur_sq, target_sq, promotion=""):
        return self.coord(cur_sq) + self.coord(target_sq) + promotion

    

    def legal_moves(self):
        # Returns list of all possible moves of one colour in UCI format
        # check for same colour piece on target square
        # this requires empty places to be 0 
        # and the colours to have opposing signs
        colour_offset = 0 if self.player_white else 6
        legal_moves = []

        def straight_moves(piece, max_step_size):
            for direction in (1, -1, 10, -10):
                for distance in range(1, max_step_size + 1):
                    target_sq = piece + direction * distance
                    if self.steppable(target_sq):
                        legal_moves.append(self.convert_to_uci(piece, target_sq))
                        #capature ends sliding move
                        if self.sq[target_sq] is not EMPTY:
                            break
                    else:
                        break

        def diagonal_moves(piece, max_step_size):
            for direction in (9, -9, 11, -11):
                for distance in range(1, max_step_size + 1):
                    target_sq = piece + direction * distance
                    if self.steppable(target_sq):
                        legal_moves.append(self.convert_to_uci(piece, target_sq))
                        if self.sq[target_sq] is not EMPTY:
                            break
                    else:
                        break
        
        
        # pawns      
        pawn_direction = -10 if self.player_white else 10
        for pawn in self.pieces[colour_offset]:
            basic = pawn + pawn_direction
            starting = pawn + pawn_direction * 2
            diagonals = [pawn + pawn_direction - 1, pawn + pawn_direction + 1]

            # Diagonal captures
            for diag in diagonals:
                if self.steppable(diag) and self.sq[diag] is not EMPTY:

                    if (self.player_white and 21 <= diag <= 28) or (
                        not self.player_white and 91 <= diag <= 98
                    ):
                        legal_moves.append(self.convert_to_uci(pawn, diag, promotion="q"))
                    else:
                        legal_moves.append(self.convert_to_uci(pawn, diag))

            #one-square pawn move
            if self.sq[basic] == EMPTY:
                if (self.player_white and 21 <= basic <= 28) or (
                    not self.player_white and 91 <= basic <= 98
                ):
                    legal_moves.append(self.convert_to_uci(pawn, basic, promotion="q"))
                else:
                    legal_moves.append(self.convert_to_uci(pawn, basic))

                # two square pawn move
                on_start = (self.player_white and 81 <= pawn <= 88) or (
                    not self.player_white and 31 <= pawn <= 38
                )
                if on_start and self.sq[starting] == EMPTY:
                    legal_moves.append(self.convert_to_uci(pawn, starting))
            
        # knights
        for knight in self.pieces[1 + colour_offset]:
            for move in [-8, -12, -19, -21, 8, 12, 19, 21]:
                target_sq = knight  + move
                if self.steppable(target_sq):
                    legal_moves.append(self.convert_to_uci(knight, target_sq))

        # bishop
        for bishop in self.pieces[2 + colour_offset]:
            diagonal_moves(bishop, 7)

        # rooks
        for rook in self.pieces[3 + colour_offset]:
            straight_moves(rook, 7)

        # queen 
        queen = self.pieces[4 + colour_offset][0]
        straight_moves(queen, 7)
        diagonal_moves(queen, 7)

        # king
        for king in self.pieces[5 + colour_offset]:
            straight_moves(king, 1)
            diagonal_moves(king, 1)

        #### TO DO ####
        # casteling
        # en passant 


        # filter out safe moves on temporary board
        safe_moves = []
        for move in legal_moves:
            source = self._uci_square(move[:2])
            target = self._uci_square(move[2:4])
            moved_piece = self.sq[source]
            captured_piece = self.sq[target] #safe content of target square 

            self.sq[target] = moved_piece
            self.sq[source] = EMPTY
            self.pieces[moved_piece].remove(source)
            self.pieces[moved_piece].append(target)
            if captured_piece not in (EMPTY, BORDER):
                self.pieces[captured_piece].remove(target)

            king_code = 5 if self.player_white else 11
            king_square = self.pieces[king_code][0]
            in_check = self.square_attacked(king_square, not self.player_white)

            #restore the original board and piece lists.
            self.sq[source] = moved_piece
            self.sq[target] = captured_piece
            self.pieces[moved_piece].remove(target)
            self.pieces[moved_piece].append(source)
            if captured_piece not in (EMPTY, BORDER):
                self.pieces[captured_piece].append(target)

            if not in_check:
                safe_moves.append(move)

        return safe_moves
    
    @staticmethod
    def _uci_square(coord):
        file_index = ord(coord[0]) - ord("a") + 1
        rank_index = 10 - int(coord[1])
        return rank_index * 10 + file_index

    def square_attacked(self, my_sqr, player_white):
        
        knight_offsets = [-21, -19, -12, -8, 8, 12, 19, 21]
        king_offset = [-10, 10, -1, 1, -11, -9, 9, 11]
        orth_offset = [10, -10, 1, -1]
        diag_offset = [-11, -9, 9, 11]

        #white turn, select attackers by the color doing the attacking
        if player_white:
            pawn_offset = [9, 11]
            orth_attackers = [3, 4]   # White rook, queen
            knight_attacker = 1       # White knight
            diag_attackers = [2, 4]   # White bishop, queen
            pawn_attacker = 0         # White pawn
            king_attacker = 5         # White king
        else:
            pawn_offset = [-9, -11]
            orth_attackers = [9, 10]  # Black rook, queen
            knight_attacker = 7       # Black knight
            diag_attackers = [8, 10]  # Black bishop, queen
            pawn_attacker = 6         # Black pawn
            king_attacker = 11        # Black king
            

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
                    break #blocked by another piece
                current_idx += offset

        #check for diagonal attacks
        for offset in diag_offset:
            current_idx = my_sqr + offset
            while self.sq[current_idx] != -1: # until hitting boundary
                if self.sq[current_idx] != None: #if non-empty square
                    if self.sq[current_idx] in diag_attackers : # bishop or queen
                        return True
                    break #blocked by another piece
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
        else:
            king_loc = self.pieces[11][0]
        return self.square_attacked(king_loc, not self.player_white)

    def is_checkmate(self):
        return self.is_check() and len(self.legal_moves()) == 0  #is in chack and no legal moves left

    def make_move(self, uci_move):
        if uci_move not in self.legal_moves():
            return False

        #make move
        source = self._uci_square(uci_move[:2])
        target = self._uci_square(uci_move[2:4])

        moved_piece = self.sq[source]
        captured_piece = self.sq[target]

        #promotion  e.g. "a7a8q"
        if len(uci_move) == 5:
            new_piece = 4 if self.player_white else 10
        else:
            new_piece = moved_piece

        # update piece lists
        self.pieces[moved_piece].remove(source)
        if captured_piece not in (EMPTY, BORDER):
            self.pieces[captured_piece].remove(target)
        self.pieces[new_piece].append(target)

        #update board squares
        self.sq[source] = EMPTY
        self.sq[target] = new_piece

        #update representation
        self.rep[source] = source
        self.rep[target] = PIECES[new_piece]

        # record move 
        self.history.append(uci_move)
        #switch turns
        self.player_white = not self.player_white

        return True

   




if __name__ == "__main__":

    board = ChessBoard()

    print(board)

    print(board.representation())

    print("White plays e2e4:", board.make_move("e2e4"))
    print("Black plays e7e5:", board.make_move("e7e5"))

    print(board.representation())
    print("Move history:", board.history)

