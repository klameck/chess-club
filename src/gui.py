"""Pygame interface with game loop"""

import pygame
import chess
import os
import threading
import queue
from game_logic import ChessGame

ASSET_DIR = os.path.join(os.path.dirname(__file__),"assets")

PIECE_FILES = {
    "K": "white_king.png",
    "Q": "white_queen.png",
    "R": "white_rook.png",
    "B": "white_bishop.png",
    "N": "white_knight.png",
    "P": "white_pawn.png",
    "k": "black_king.png",
    "q": "black_queen.png",
    "r": "black_rook.png",
    "b": "black_bishop.png",
    "n": "black_knight.png",
    "p": "black_pawn.png",
}

# board settings
WINDOW_SIZE = 640
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8
MESSAGE_HEIGHT = 40
MESSAGE_BACKGROUND = (35, 35, 35)
MESSAGE_COLOR = (255, 255, 255)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (71, 110, 58)
BACKGROUND = (35, 35, 35)
# end screen
RESULT_BACKGROUND = (35, 35, 35)
RESULT_TEXT_COLOR = (255, 255, 255)

BUTTON_COLOR = (71, 110, 58)
BUTTON_HOVER_COLOR = (240, 217, 181)
BUTTON_TEXT_COLOR = (255, 255, 255)

BUTTON_WIDTH = 160
BUTTON_HEIGHT = 48


class ChessGUI:
    def __init__(self, game):
        pygame.init()

        # set screen
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + MESSAGE_HEIGHT))
        pygame.display.set_caption("Play against Stockfish!")

        self.clock = pygame.time.Clock()
        
        self.game = game
        self.board = self.game.board
        self.running = True
        #messages
        self.font = pygame.font.SysFont("Arial", 20)
        self.message = "White to move"
        #ending screen
        self.game_over = False
        self.result_text = ""
        self.reason_text = ""
        self.quit_button = pygame.Rect(90, 480, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.rematch_button = pygame.Rect(390, 480, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.button_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.result_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.detail_font = pygame.font.SysFont("Arial", 20)

        self.engine_thinking = False
        self.engine_results = queue.Queue()

        #pieces
        self.piece_images = {}
        self.selected_square = None
        for symbol, filename in PIECE_FILES.items():
            path = os.path.join(ASSET_DIR, filename)
            image = pygame.image.load(path).convert_alpha()

            self.piece_images[symbol] = pygame.transform.smoothscale(
                image,
                (SQUARE_SIZE, SQUARE_SIZE)
            )


    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = (
                    LIGHT_SQUARE
                    if (row + col) % 2 == 0
                    else DARK_SQUARE
                )

                rect = pygame.Rect(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )
                pygame.draw.rect(self.screen, color, rect)

    def draw_pieces(self):
        for square, piece in self.board.piece_map().items():
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)

            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE

            image = self.piece_images[piece.symbol()]
            self.screen.blit(image, (x, y))

    def draw_message(self):
        rect = pygame.Rect(0, BOARD_SIZE, WINDOW_SIZE, MESSAGE_HEIGHT)
        pygame.draw.rect(self.screen, MESSAGE_BACKGROUND, rect)
        self.font = pygame.font.SysFont("Arial",20,)
        text = self.font.render(self.message,True, (255, 255, 255) ,)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, BOARD_SIZE + MESSAGE_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def draw_selection(self):
            if self.selected_square is None:
                return
    
            col = chess.square_file(self.selected_square)
            row = 7 - chess.square_rank(self.selected_square)
    
            rect = pygame.Rect(
                col * SQUARE_SIZE,
                row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )
    
            pygame.draw.rect(
                self.screen,
                (80, 180, 80),
                rect,
                width=4,
            )

    def handle_click(self, position):
        if self.engine_thinking or self.game.is_game_over():
            return

        # human is playing white
        if self.game.current_turn() != "White":
            return

        x, y = position
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        if not (0 <= col < 8 and 0 <= row < 8):
            return

        square = chess.square(col, 7 - row)

        # First click -> select White piece.
        if self.selected_square is None:
            piece = self.board.piece_at(square)

            if piece is not None and piece.color == chess.WHITE:
                self.selected_square = square
                self.message = f"Selected {chess.square_name(square)}"
            else:
                self.message = "Select one of your white pieces"

            return

        # Clicking another White piece changes the selection.
        target_piece = self.board.piece_at(square)

        if target_piece is not None and target_piece.color == chess.WHITE:
            self.selected_square = square
            self.message = f"Selected {chess.square_name(square)}"
            return

        move = chess.Move(self.selected_square, square)

        # Automatically promotes pawn to queen !!! ################change later ###########
        piece = self.board.piece_at(self.selected_square)
        if (
            piece is not None
            and piece.piece_type == chess.PAWN
            and chess.square_rank(square) in (0, 7)
        ):
            move.promotion = chess.QUEEN

        # validate and apply the move.
        success, result = self.game.human_move(move.uci())
        self.selected_square = None

        if not success:
            self.message = result
            return

        self.message = f"You played {result}"

        # Start Stockfish after successful human move
        if not self.game.is_game_over():
            self.request_engine_move()


    def request_engine_move(self):
        if self.engine_thinking or self.game.is_game_over():
            return

        self.engine_thinking = True
        self.message = "Stockfish is thinking..."

        def worker():
            try:
                result = self.game.engine_move()
                self.engine_results.put(("success", result))
            except Exception as exc:
                self.engine_results.put(("error", str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def draw_button(self, rect, text):
        mouse_pos = pygame.mouse.get_pos()

        color = (
            BUTTON_HOVER_COLOR
            if rect.collidepoint(mouse_pos)
            else BUTTON_COLOR
        )

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=10,
        )

        label = self.button_font.render(
            text, True, BUTTON_TEXT_COLOR
        )
        self.screen.blit(label, label.get_rect(center=rect.center))

    def show_game_over(self):
        result, reason = self.game.game_result()

        if result == "1-0":
            self.result_text = "White wins!"
        elif result == "0-1":
            self.result_text = "Black wins!"
        else:
            self.result_text = "It's a draw!"

        self.reason_text = reason.replace("_", " ").title()
        self.game_over = True

    def handle_game_over_click(self, position):
        print("Clicked at:", position)

        if self.quit_button.collidepoint(position):
            print("Quit clicked")
            self.running = False

        elif self.rematch_button.collidepoint(position):
            print("Rematch clicked")
            engine = self.game.engine
            self.game = ChessGame(engine=engine)
            self.board = self.game.board
            self.selected_square = None
            self.engine_thinking = False
            self.game_over = False
            self.result_text = ""
            self.reason_text = ""
            self.message = "White to move"

    def draw_game_over(self):
        self.screen.fill(RESULT_BACKGROUND)

        title = self.result_font.render(
            "Game Over", True, RESULT_TEXT_COLOR
        )
        self.screen.blit(
            title,
            title.get_rect(center=(WINDOW_SIZE // 2, 180)),
        )

        result = self.detail_font.render(
            self.result_text, True, RESULT_TEXT_COLOR
        )
        self.screen.blit(
            result,
            result.get_rect(center=(WINDOW_SIZE // 2, 250)),
        )

        reason = self.detail_font.render(
            f"Reason: {self.reason_text}",
            True,
            RESULT_TEXT_COLOR,
        )
        self.screen.blit(
            reason,
            reason.get_rect(center=(WINDOW_SIZE // 2, 295)),
        )

        self.draw_button(self.quit_button, "Quit")
        self.draw_button(self.rematch_button, "Rematch")

    def run(self):
        while self.running:

            # window events 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.game_over:
                            self.handle_game_over_click(event.pos)
                        else:
                            # handle clicks and turns
                            self.handle_click(event.pos)

            # check engine
            if self.engine_thinking:
                try:
                    status, result = self.engine_results.get_nowait()
                    self.engine_thinking = False

                    if status == "error":
                        self.message = f"Engine error: {result}"
                        print(self.message)
                    elif result is None:
                        self.message = "No engine move available"
                    else:
                        self.message = f"Stockfish played: {result}"

                except queue.Empty:
                    pass

            #switch to end screen
            if not self.game_over and self.game.is_game_over():
                self.show_game_over()

            if self.game_over:
                self.draw_game_over()
            else:
                self.draw_board()
                self.draw_pieces()
                self.draw_selection()
                self.draw_message()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


