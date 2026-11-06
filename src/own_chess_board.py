"""
The board should mimic the basic interface of a python-chess board. 
"""

"""
TO DO
- draw rules
- fen notation

- en passant
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

class MyBoard():
    """Standard 8x8 board in a 10x12 mailbox (120 repuares, index = row*12 + col).
    Off-board repuares are OFF (-1), so edge moves need no bounds checks."""

    def __init__(self, fen: str | None = None):
        
        self.en_passant = None
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.castling_history = []
        self.sq = [EMPTY] * 120
        self.rep = list(range(120))
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
        self.capture_history = []
        self.en_passant_captured_sq = []
        # white starts
        self.player_white = True 

        # track if castling is still possibel
        self.castling_rights = {"w_king_side" : True, "w_queen_side" : True, "b_king_side" : True, "b_queen_side" : True}
        
        #fen notation 
        if fen is not None:
            self.load_fen(fen)
        else:
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
        
        self.fen = self.to_fen()


    def __str__(self):
        return "\n".join(
            " ".join(f"{self.sq[rank*10 + file]}" 
            for file in range(0, 10)) 
            for rank in range(0, 12)
        ) + "\n\n"

    def load_fen(self, fen):
        self.history = []
        self.capture_history = []

        parts = fen.split()

        if len(parts) != 6:
            raise ValueError("Invalid FEN: expected 6 fields")

        piece_placement, active_color, castling, ep, halfmove, fullmove = parts

        # Clear the playable squares and piece lists
        for rank in range(8):
            for file in range(1, 9):
                self.sq[rank * 10 + 21 + file - 1] = EMPTY

        self.pieces = [[] for _ in range(12)]

        # Set up pieces
        ranks = piece_placement.split("/")

        if len(ranks) != 8:
            raise ValueError("Invalid FEN: expected 8 ranks")

        for rank_index, rank_data in enumerate(ranks):
            file_index = 0

            for char in rank_data:
                if char.isdigit():
                    file_index += int(char)
                else:
                    piece_code = next(
                        code for code, symbol in PIECES.items()
                        if symbol == char
                    )

                    square = 21 + rank_index * 10 + file_index

                    self.sq[square] = piece_code
                    self.pieces[piece_code].append(square)

                    file_index += 1

            if file_index != 8:
                raise ValueError("Invalid FEN: rank does not contain 8 squares")

        # Active player
        self.player_white = active_color == "w"

        # Castling rights
        self.castling_rights = {
            "w_king_side": "K" in castling,
            "w_queen_side": "Q" in castling,
            "b_king_side": "k" in castling,
            "b_queen_side": "q" in castling
        }
        # En-passant target square
        self.en_passant = None if ep == "-" else self._from_uci(ep)

        # Move counters
        self.halfmove_clock = int(halfmove)
        self.fullmove_number = int(fullmove)

        self.history = []
        self.fen = fen

    def to_fen(self):
        rows = []

        for rank in range(8):
            row = ""
            empty_count = 0

            for file in range(8):
                square = 21 + rank * 10 + file
                piece = self.sq[square]

                if piece == EMPTY:
                    empty_count += 1
                else:
                    if empty_count:
                        row += str(empty_count)
                        empty_count = 0

                    row += PIECES[piece]

            if empty_count:
                row += str(empty_count)

            rows.append(row)

        piece_placement = "/".join(rows)

        active_color = "w" if self.player_white else "b"

        castling = ""
        if self.castling_rights["w_king_side"]:
            castling += "K"

        if self.castling_rights["w_queen_side"]:
            castling += "Q"

        if self.castling_rights["b_king_side"]:
            castling += "k"

        if self.castling_rights["b_queen_side"]:
            castling += "q"

        if not castling:
            castling = "-"
       

        ep = "-" if self.en_passant is None else self.coord(self.en_passant)

        return (
            f"{piece_placement} {active_color} {castling} "
            f"{ep} {self.halfmove_clock} {self.fullmove_number}"
        )

    
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

    def do_castling(self, legal_moves):

        if self.player_white:
            #white kingside e1 to g1
            if (
                self.castling_rights["w_king_side"]
                and self.sq[98] == 3       # white rook on h1
                and self.sq[96] is EMPTY   # f1 empty
                and self.sq[97] is EMPTY   # g1 empty
                #check if kings path is under attack
                and not self.square_attacked(95)
                and not self.square_attacked(96)
                and not self.square_attacked(97)
            ):
                legal_moves.append("e1g1")

            #white queen side e1 to c1
            if (
                self.castling_rights["w_queen_side"]
                and self.sq[91] == 3       # white rook on a1
                and self.sq[92] is EMPTY  
                and self.sq[94] is EMPTY   # d1 empty
                and self.sq[93] is EMPTY   # c1 empty
                #check if kings path is under attack
                and not self.square_attacked(95)
                and not self.square_attacked(94)
                and not self.square_attacked(93)
            ):
                legal_moves.append("e1c1")
        else:
            #black kingside e8 to g8
            if (
                self.castling_rights["b_king_side"]
                and self.sq[28] == 9       # black rook on h8
                and self.sq[27] is EMPTY   
                and self.sq[26] is EMPTY   
                #check if kings path is under attack
                and not self.square_attacked(25)
                and not self.square_attacked(26)
                and not self.square_attacked(27)
            ):
                legal_moves.append("e8g8")

            #black queen side e8 to c8
            if (
                self.castling_rights["b_queen_side"]
                and self.sq[21] == 9       # black rook on a8
                and self.sq[22] is EMPTY  
                and self.sq[24] is EMPTY   
                and self.sq[23] is EMPTY  
                #check if kings path is under attack
                and not self.square_attacked(24)
                and not self.square_attacked(25)
                and not self.square_attacked(23)
            ):
                legal_moves.append("e8c8")

        return
    

    def get_legal_moves(self):
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
        for queen in self.pieces[4 + colour_offset]:
            straight_moves(queen, 7)
            diagonal_moves(queen, 7)

        # king
        king = self.pieces[5 + colour_offset][0]
        straight_moves(king, 1)
        diagonal_moves(king, 1)

        #castling
        self.do_castling(legal_moves)

        # en passant
        pawn_starting_moves = ["a2a4", "b2b4", "c2c4", "d2d4", "e2e4", "f2f4", "g2g4", "h2h4", "a7a5", "b7b5", "c7c5", "d7d5", "e7e5", "f7f5", "g7g5", "h7h5"]
        # last move of phistoryotentially captured pawn was starting move (double advance)
        if len(self.history) > 0 and self.history[-1] in pawn_starting_moves:
            # check only adjacant files / chapturing pawn has advanced exactly three
            capture_square = self._from_uci(self.history[-1][2:4])
            for attacking_square in [capture_square +1, capture_square -1]:
                if self.player_white and self.sq[attacking_square] == 0 or not self.player_white and self.sq[attacking_square] == 6:
                    legal_moves.append(self.convert_to_uci(attacking_square, capture_square + pawn_direction))


        # filter out safe moves on temporary board
        safe_moves = []
        for move in legal_moves:
            source = self._from_uci(move[:2])
            target = self._from_uci(move[2:4])
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
            in_check = self.square_attacked(king_square)

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
    def _from_uci(coord):
        file_index = ord(coord[0]) - ord("a") + 1
        rank_index = 10 - int(coord[1])
        return rank_index * 10 + file_index

    def square_attacked(self, my_sqr):
        
        knight_offsets = [-21, -19, -12, -8, 8, 12, 19, 21]
        king_offset = [-10, 10, -1, 1, -11, -9, 9, 11]
        orth_offset = [10, -10, 1, -1]
        diag_offset = [-11, -9, 9, 11]

        #white turn, select attackers by the color doing the attacking
        if self.player_white:
            pawn_offset = [-9, -11]
            
            orth_attackers = [9, 10]  # Black rook, queen
            knight_attacker = 7       # Black knight
            diag_attackers = [8, 10]  # Black bishop, queen
            pawn_attacker = 6         # Black pawn
            king_attacker = 11        # Black king
            
        else:
            pawn_offset = [9, 11]
            
            orth_attackers = [3, 4]   # White rook, queen
            knight_attacker = 1       # White knight
            diag_attackers = [2, 4]   # White bishop, queen
            pawn_attacker = 0         # White pawn
            king_attacker = 5         # White king

            
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

        return self.square_attacked(king_loc)

    def is_checkmate(self):
        return self.is_check() and len(self.get_legal_moves()) == 0  #is in check and no legal moves left


    def is_draw(self):
        # stalemate
        if len(self.get_legal_moves()) == 0:
            return True 
        # insufficient material
        # combination of any of these (without pawns)
        # a lone king
        # king + bishop
        # king + knight

        # king + 2 knights v. king

        # 50 Move rule
        # if no pawn has been moved and no capture has been made in the last 50 moves.

        # Draw by repition
        # third time same board state (requires full history)

    def move_rook(self, source, target):
        rook = self.sq[source]

        self.sq[source] = EMPTY
        self.sq[target] = rook

        self.pieces[rook].remove(source)
        self.pieces[rook].append(target)

        self.rep[source] = "."
        self.rep[target] = PIECES[rook]
    
    def push_move(self, uci_move):
        if uci_move not in self.get_legal_moves():
            return False

        #save castling history
        self.castling_history.append(self.castling_rights.copy())

        #make move
        source = self._from_uci(uci_move[:2])
        target = self._from_uci(uci_move[2:4])

        moved_piece = self.sq[source]
        captured_piece = self.sq[target]
        en_passant_sq = None

        # en passant
        if self.sq[source] in [0, 6] and abs(source - target) in [9, 11] and self.sq[target] == EMPTY:
            direction = 10 if self.player_white else -10 
            en_passant_sq = target + direction
            captured_piece = self.sq[en_passant_sq]
        
        # Update castling rights
        if moved_piece == 5 :  # White king
            self.castling_rights["w_king_side"] = False
            self.castling_rights["w_queen_side"] = False

        elif moved_piece == 11:  # Black king
            self.castling_rights["b_king_side"] = False
            self.castling_rights["b_queen_side"] = False
        rook_rights = {
            98: "w_king_side",  # White h1
            91: "w_queen_side",  # White a1
            28: "b_king_side",  # Black h8
            21: "b_queen_side"   # Black a8
        }
        if source in rook_rights:
            self.castling_rights[rook_rights[source]] = False
        if target in rook_rights and captured_piece in (3, 9):
            self.castling_rights[rook_rights[target]] = False

        # Halfmove clock
        if moved_piece in (0, 6) or captured_piece not in (EMPTY, BORDER):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # promotion  e.g. "a7a8q"
        if len(uci_move) == 5:
            new_piece = 4 if self.player_white else 10
        else:
            new_piece = moved_piece

        # update piece lists
        self.pieces[moved_piece].remove(source)
        if captured_piece not in (EMPTY, BORDER):
            if en_passant_sq == None:
                self.pieces[captured_piece].remove(target)
            else:
                self.pieces[captured_piece].remove(en_passant_sq)
        self.pieces[new_piece].append(target)

        # update board squares
        self.sq[source] = EMPTY
        self.sq[target] = new_piece
        if en_passant_sq != None:
            self.sq[en_passant_sq] = EMPTY

        # Castling-> move rook 
        if uci_move == "e1g1":  # White kingside
            self.move_rook(98, 96)
        elif uci_move == "e1c1":  # White queenside
            self.move_rook(91, 94)
        elif uci_move == "e8g8":  # Black kingside
            self.move_rook(28, 26)
        elif uci_move == "e8c8":  # Black queenside
            self.move_rook(21, 24)

        # update representation
        self.rep[source] = source
        self.rep[target] = PIECES[new_piece]

        # record move 
        self.history.append(uci_move)
        self.capture_history.append(captured_piece)
        self.en_passant_captured_sq.append(en_passant_sq)
        #switch turns
        self.player_white = not self.player_white
        if not self.player_white:
            self.fullmove_number += 1
        self.fen = self.to_fen()


        return True

    def pop_move(self) -> None:
        """Reverts the last executed move, restoring the previous board state."""
        
        # get last move and remove from history
        uci_move = self.history.pop()
        source = self._from_uci(uci_move[:2])
        target = self._from_uci(uci_move[2:4])
        moved_piece = self.sq[target]

        captured_piece = self.capture_history.pop()
        self.castling_rights = self.castling_history.pop()
        
        # undo promotion  e.g. "a7a8q"
        if len(uci_move) == 5:
            old_piece = 0 if self.player_white else 6
        else:
            old_piece = moved_piece

        # undo casteling
        # Castling-> move rook 
        if uci_move == "e1g1":  # White kingside
            self.move_rook(96, 98)
            self.castling_rights["w_king_side"] = True
        elif uci_move == "e1c1":  # White queenside
            self.move_rook(94, 91)
            self.castling_rights["w_queen_side"] = True                  
        elif uci_move == "e8g8":  # Black kingside
            self.move_rook(26, 28)
            self.castling_rights["b_king_side"] = True
        elif uci_move == "e8c8":  # Black queenside
            self.move_rook(24, 21)
            self.castling_rights["b_queen_side"] = True

        
        # move piece back
        # update piece lists
        self.pieces[moved_piece].remove(target)
        self.pieces[old_piece].append(source)

        # re-put captured piece
        en_passant = self.en_passant_captured_sq.pop()
        if captured_piece not in (EMPTY, BORDER):
            # check for en passant
            if en_passant == None:
                self.pieces[captured_piece].append(target)
            else:
                self.pieces[captured_piece].append(en_passant)
    
        

        # update board squares
        self.sq[source] = old_piece
        if en_passant == None:
            self.sq[target] = captured_piece
        else:
            self.sq[en_passant] = captured_piece
            self.sq[target] = EMPTY
    

        # update representation
        #self.rep[target] = target if captured_piece == EMPTY else captured_piece
        #self.rep[source] = PIECES[old_piece]

        # player
        self.player_white = not self.player_white


def test_moves(board, move):
    """
    For testing (special) moves
    c: castling
    ep: en passant
    """
    if move == "c":
        print("test castling")
        # Clear the pieces between the white king and rook
        for square in [96, 97]:
            piece = board.sq[square]
            if piece is not EMPTY:
                board.pieces[piece].remove(square)
                board.sq[square] = EMPTY
        print("Black plays e7e5:", board.push_move("e1g1"))
        print(board.representation())
    elif move == "ep":
        print("testing en passant")
        print("White moves d2d4", board.push_move("d2d4"))
        print("Black moves g8h6", board.push_move("g8h6"))
        print("White moves d4d5", board.push_move("d4d5"))
        print("Black moves c7c5", board.push_move("c7c5"))
        print(board.representation())
        print("White moves d5c6", board.push_move("d5c6"))
        print(board.representation())

        print("Reversing last move", board.pop_move())
        print(board.representation())

    else:
        try:
            board.push_move(move)
        except:
            print("Try using a valid option, 'c', 'ep' or a move in uci notation.") 




if __name__ == "__main__":

    """board = ChessBoard()

    print(board)

    print(board.representation())
    print(board.fen)

    print("White plays e2e4:", board.push_move("e2e4"))
    print("Black plays e7e5:", board.push_move("e7e5"))
    print("Undo last move", board.pop_move())

    print(board.representation())
    print("Move history:", board.history)"""

    # Standard starting position
    #board = ChessBoard()
    """
    print(board.to_fen())

    # Load standard starting position from FEN
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    board2 = ChessBoard(fen)

    print(board2.to_fen())
    print(board2.representation())

    # Make a move
    board2.push_move("e2e4")
    print(board2.representation())

    print(board2.to_fen())
    """
    # Kiwi-Pete
    fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
    board = MyBoard(fen)
    print(board.representation())
    print(board.push_move("a2a4"))
    print(board.representation())
    print(board.push_move("b4a3"))
    #test_moves(board, "ep")


