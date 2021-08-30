
from typing import cast

from logging import Logger
from logging import getLogger

from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.model.Coordinates import Coordinates


class FutureEvent:

    def __init__(self, futureEventType: FutureEventType, starDate: float = 0.0, quadrantCoordinates: Coordinates = cast(Coordinates, None)):
        """

        Args:
            futureEventType:        The event type
            starDate:               When it is supposed to happen
            quadrantCoordinates:    Which Quadrant it applies to
        """

        self.logger: Logger = getLogger(__name__)

        self._eventType:           FutureEventType = futureEventType
        self._starDate:            float           = starDate
        self._quadrantCoordinates: Coordinates     = quadrantCoordinates

    @property
    def type(self) -> FutureEventType:
        return self._eventType

    @type.setter
    def type(self, theNewValue: FutureEventType):
        self._eventType = theNewValue

    @property
    def starDate(self) -> float:
        return self._starDate

    @starDate.setter
    def starDate(self, theNewValue: float):
        self._starDate = theNewValue

    @property
    def quadrantCoordinates(self) -> Coordinates:
        return self._quadrantCoordinates

    @quadrantCoordinates.setter
    def quadrantCoordinates(self, theNewValue: Coordinates):
        self._quadrantCoordinates = theNewValue

    def __repr__(self):

        representation = (
            f"eventType: {self._eventType.name:8} "
            f"starDate: {self._starDate:5.2f} "
            f"qCoordinates: '{self._quadrantCoordinates}'"
        )
        return representation
