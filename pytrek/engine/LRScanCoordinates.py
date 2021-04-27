
from dataclasses import dataclass

from pytrek.engine.Direction import Direction
from pytrek.model.Coordinates import Coordinates


@dataclass
class LRScanCoordinates:
    """
    This data object classifies coordinates for the method Intelligence.generateAdjacentCoordinates.
    It indicates the coordinate value and the direction from the center quadrant;  Aka,
    where the Enterprise is located

    """

    coordinates: Coordinates = Coordinates(x=0, y=0)
    direction:   Direction   = Direction.North
