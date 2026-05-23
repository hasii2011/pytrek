
from dataclasses import field
from dataclasses import dataclass

from pytrek.engine.Direction import Direction

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Coordinates import coordinateFactory


@dataclass
class DirectionData:

    coordinates: Coordinates = field(default_factory=coordinateFactory)
    direction:   Direction   = Direction.North
