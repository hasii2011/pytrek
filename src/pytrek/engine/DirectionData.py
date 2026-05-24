
from dataclasses import field
from dataclasses import dataclass

from src.pytrek.engine.Direction import Direction

from src.pytrek.model.Coordinates import Coordinates
from src.pytrek.model.Coordinates import coordinateFactory


@dataclass
class DirectionData:

    coordinates: Coordinates = field(default_factory=coordinateFactory)
    direction:   Direction   = Direction.North
