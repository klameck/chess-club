"""Game logic with rules and game states"""
import chess

class ChessGame:
    def __init__(self, engine):
        self.board = chess.Board()
        self.engine = engine

    def human_move(self, user_move):
        "Validate and apply user move"
        try:
            move = self.board.parse_uci(user_move)
        except ValueError:
            return False, "Illegal move."

        # update board
        san = self.board.san(move)
        self.board.push(move)

        return True, san

    def engine_move(self):
        #get all played moves
        moves = [move.uci() for move in self.board.move_stack]

        #get best move
        best_move = self.engine.get_best_move(moves=moves)

        # check and apply move
        try:
            move = self.board.parse_uci(best_move)
        except ValueError as exc:
            raise RuntimeError(
                f"Engine returned an illegal move: {best_move}"
            ) from exc

        # update board
        san = self.board.san(move)
        self.board.push(move)

        return san

    def is_game_over(self):
        #check if game ended
        return self.board.is_game_over(claim_draw=True)

    def game_result(self):
        #game result 
        outcome = self.board.outcome(claim_draw=True)

        if outcome is None:
            return None

        return outcome.result(), outcome.termination.name

    def current_turn(self):
        return "White" if self.board.turn == chess.WHITE else "Black"

