
from dataclasses import dataclass
from dataclasses import field

from pytrek.model.Coordinates import Coordinates


def coordinateFactory() -> Coordinates:
    return Coordinates()


@dataclass
class AutomaticMoveData:

    sectorMove: bool = False

    quadrantCoordinates: Coordinates = field(default_factory=coordinateFactory)
    sectorCoordinates:   Coordinates = field(default_factory=coordinateFactory)
