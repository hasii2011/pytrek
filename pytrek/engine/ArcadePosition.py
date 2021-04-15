
from dataclasses import dataclass


@dataclass
class ArcadePosition:
    """
    Represent the position of arcade sprites.
    """
    x: float = 0.0
    y: float = 0.0

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return f"ArcadePosition({self.x},{self.y})"

    def __eq__(self, other) -> bool:
        if isinstance(other, ArcadePosition):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            return False

