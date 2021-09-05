
from typing import cast

from dataclasses import dataclass

from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.model.Coordinates import Coordinates


@dataclass
class FutureEvent:
    """
    An Event something that happens in a quadrant at a particular time.
    """
    type:                FutureEventType = cast(FutureEventType, None)
    quadrantCoordinates: Coordinates     = cast(Coordinates, None)
    starDate:            float           = 0.0

    def __repr__(self):

        representation = (
            f"eventType: {self.type.name:8} "
            f"starDate: {self.starDate:5.2f} "
            f"qCoordinates: '{self.quadrantCoordinates}'"
        )
        return representation
