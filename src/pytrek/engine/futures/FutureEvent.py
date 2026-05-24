
from typing import cast
from typing import Callable

from dataclasses import dataclass

from src.pytrek.engine.futures.FutureEventType import FutureEventType

from src.pytrek.model.Coordinates import Coordinates


EventCallback = Callable[['FutureEvent'], None]


@dataclass
class FutureEvent:
    """
    An Event something that happens in a quadrant at a particular time.
    When conditions change in the game that make a certain type of event
    irrelevant the event handlers set schedulable to False;
    For example, if all commanders are dead, then commanders cannot attack
    or destroy a base
    """
    type:                FutureEventType = cast(FutureEventType, None)
    quadrantCoordinates: Coordinates     = cast(Coordinates, None)
    starDate:            float    = 0.0
    callback:            EventCallback   = cast(EventCallback, None)
    schedulable:         bool            = True

    def __repr__(self):

        representation = (
            f"eventType: {self.type.name:8} "
            f"starDate: {self.starDate:5.2f} "
            f"qCoordinates: '{self.quadrantCoordinates}' "
            f"schedulable: '{self.schedulable}'"
        )
        return representation
