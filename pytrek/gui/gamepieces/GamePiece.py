
from typing import cast

from arcade import Sprite

from pytrek.Constants import STANDARD_SPRITE_HEIGHT
from pytrek.Constants import STANDARD_SPRITE_WIDTH
from pytrek.Constants import STANDARD_X_ADJUSTMENT
from pytrek.Constants import STANDARD_Y_ADJUSTMENT
from pytrek.model.Coordinates import Coordinates


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

    def gamePositionToScreenPosition(self, gameCoordinates: Coordinates):

        sectorX: int = gameCoordinates.x
        sectorY: int = gameCoordinates.y
        x = ((sectorX * STANDARD_SPRITE_WIDTH)  * 2) + STANDARD_X_ADJUSTMENT
        y = ((sectorY * STANDARD_SPRITE_HEIGHT) * 2) + STANDARD_Y_ADJUSTMENT

        return x, y
