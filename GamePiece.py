
from typing import cast

from arcade import Sprite

from pytrek.objects.Coordinates import Coordinates


class GamePiece(Sprite):

    def __init__(self):
        super().__init__()

        self._currentPosition: Coordinates = cast(Coordinates, None)

    @property
    def currentPosition(self) -> Coordinates:
        return self._currentPosition

    @currentPosition.setter
    def currentPosition(self, newValue: Coordinates):
        self._currentPosition = newValue
