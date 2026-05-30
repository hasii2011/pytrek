
from dataclasses import dataclass
from dataclasses import field

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Coordinates import coordinateFactory


@dataclass
class AutomaticMoveData:
    """
    If sector move is True then ignore the quadrant coordinates
    """

    sectorMove: bool = False

    quadrantCoordinates: Coordinates = field(default_factory=coordinateFactory)
    sectorCoordinates:   Coordinates = field(default_factory=coordinateFactory)
