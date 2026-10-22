"""Start game"""
from pathlib import Path
import platform
from game_logic import ChessGame
from engine import UCIEngine
from gui import ChessGUI

def main():

    # locate stock fish
    system = platform.system()
    if system == "Windows":
        engine_name = "stockfish-windows-x86-64-universal.exe"
    elif system == "Linux":
        engine_name = "stockfish-linux-x86-64-universal"
    else:
        raise OSError(f"Unsupported operating system: {system}")

    engine_path = Path(__file__).parent / "stockfish" / engine_name

    if not engine_path.is_file():
        raise FileNotFoundError(
            f"Stockfish executable not found: {engine_path}"
        )

    
    # start up everything
    engine = UCIEngine(str(engine_path))

    try:
        game = ChessGame(engine)
        gui = ChessGUI(game)
        gui.run()
    finally:
        engine.close()

    

if __name__ == "__main__":
    main()