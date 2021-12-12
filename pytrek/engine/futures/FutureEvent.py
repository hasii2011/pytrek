
from typing import Callable
from typing import NewType
from typing import cast

from dataclasses import dataclass

from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.model.Coordinates import Coordinates


EventCallback = NewType('EventCallback', Callable[['FutureEvent'], None])  # type: ignore


@dataclass
class FutureEvent:
    """
    An Event something that happens in a quadrant at a particular time.
    """
    type:                FutureEventType = cast(FutureEventType, None)
    quadrantCoordinates: Coordinates     = cast(Coordinates, None)
    starDate:            float           = 0.0
    callback:            EventCallback   = cast(EventCallback, None)

    def __repr__(self):

        representation = (
            f"eventType: {self.type.name:8} "
            f"starDate: {self.starDate:5.2f} "
            f"qCoordinates: '{self.quadrantCoordinates}'"
        )
        return representation
