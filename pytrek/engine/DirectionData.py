
from dataclasses import dataclass

from pytrek.engine.Direction import Direction
from pytrek.model.Coordinates import Coordinates


@dataclass
class DirectionData:

    coordinates: Coordinates = Coordinates(x=0, y=0)
    direction:   Direction   = Direction.North
