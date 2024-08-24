
from dataclasses import dataclass


@dataclass
class ManualMoveData:
    """
    Less than 1 values should be processed as moves within the quadrants (e.g. .1 .1)
    greater than one moves are deltas within the galaxy
    """
    deltaX: float = 0.0
    deltaY: float = 0.0
