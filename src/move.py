from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Move:
    from_square: int
    to_square: int
    promotion: int = -1

    def __str__(self):
        return f"{self.from_square}->{self.to_square}"
