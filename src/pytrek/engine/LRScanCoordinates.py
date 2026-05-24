
from dataclasses import field
from dataclasses import dataclass

from pytrek.engine.Direction import Direction

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Coordinates import coordinateFactory


@dataclass
class LRScanCoordinates:
    """
    This data object classifies coordinates for the method Intelligence.generateAdjacentCoordinates.
    It indicates the coordinate value and the direction from the center quadrant;  Aka,
    here the Enterprise is located

    """

    coordinates: Coordinates = field(default_factory=coordinateFactory)
    direction:   Direction   = Direction.North
