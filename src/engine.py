"""Manage Stockfish communication"""
import subprocess

class UCIEngine:
    def __init__(self, engine_path):
        self.process = subprocess.Popen(
            [engine_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def send_command(self, command):
        """Writes a text command to the engine's stdin."""
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()  # Forces data out of Python's buffer immediately

    def read_line(self) -> str:
        """Reads a single line of text from the engine's stdout."""
        return self.process.stdout.readline().strip()

    def start(self):
        """Perform the UCI and readiness handshakes."""
        self.send_command("uci")

        while True:
            line = self.read_line()
            print(f"[Engine]: {line}")
            if line == "uciok":
                break

        self.send_command("isready")

        if self.read_line() == "readyok":
            print("Engine is fully initialized!")

    def get_best_move(self, movetime=500, moves=None):
        """Request and return Stockfish's best move in UCI notation."""
        position = "position startpos"
        if moves:
            position += " moves " + " ".join(moves)

        self.send_command(position)
        self.send_command(f"go movetime {movetime}")

        while True:
            line = self.read_line()

            if line.startswith("bestmove"):
                parts = line.split()
                return parts[1] if len(parts) > 1 else None

    def close(self):
        """Shut down Stockfish."""
        if self.process.poll() is None:
            self.send_command("quit")
            self.process.wait()

        if self.process.stdin:
            self.process.stdin.close()

        if self.process.stdout:
            self.process.stdout.close()

