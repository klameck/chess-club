
"""Game logic using own ChessBoard class."""

from own_chess_board import ChessBoard


class ChessGame:
    def __init__(self, engine):
        self.board = ChessBoard()
        self.engine = engine

    def human_move(self, user_move):
        """Validate and apply a human move in UCI format."""
        if not self.board.make_move(user_move):
            return False, "Illegal move."

        # SAN notation is not implemented yet, so return UCI.
        return True, user_move

    def engine_move(self):
        """Ask the engine for a move and apply it."""
        if self.is_game_over():
            raise RuntimeError("The game is already over.")

        # history of moves
        moves = self.board.history

        best_move = self.engine.get_best_move(moves=moves)

        if not self.board.make_move(best_move):
            raise RuntimeError(
                f"Engine returned an illegal move: {best_move}"
            )

        return best_move

    def is_game_over(self):
        """Detect checkmate or stalemate."""
        return len(self.board.legal_moves()) == 0

    def game_result(self):
        """Return the result and reason, or None if the game continues."""
        if not self.is_game_over():
            return None

        if self.board.is_check():
            winner = "Black" if self.board.player_white else "White"
            result = "0-1" if winner == "Black" else "1-0"
            return result, "CHECKMATE"

        return "1/2-1/2", "STALEMATE"

    def current_turn(self):
        return "White" if self.board.player_white else "Black"
