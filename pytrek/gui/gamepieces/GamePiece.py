
from typing import cast

from arcade import Sprite

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_MARGIN
from pytrek.Constants import QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_ROWS

from pytrek.model.Coordinates import Coordinates


class GamePiece(Sprite):

    def __init__(self, filename: str = None, scale: float = 1.0):

        super().__init__(filename=filename, scale=scale)

        self._currentPosition: Coordinates = cast(Coordinates, None)

        self._speed: float = 2
        """
        Max speed
        """
        self._rotationSpeed: float = 3
        """
        Max speed we can rotate
        """

    @property
    def currentPosition(self) -> Coordinates:
        """

        Returns:  The current quadrant position
        """
        return self._currentPosition

    @currentPosition.setter
    def currentPosition(self, newValue: Coordinates):
        self._currentPosition = newValue

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, newValue: float):
        self._speed = newValue

    @property
    def rotationSpeed(self) -> float:
        return self._rotationSpeed

    @rotationSpeed.setter
    def rotationSpeed(self, newValue: float):
        self._rotationSpeed = newValue

    @classmethod
    def gamePositionToScreenPosition(cls, gameCoordinates: Coordinates):

        sectorX: int = gameCoordinates.x
        sectorY: int = gameCoordinates.y
        #
        # because game coordinates are top L - R and down
        # and game coordinates are 0-based
        adjustSectorX: int = sectorX
        adjustSectorY: int = (QUADRANT_ROWS - sectorY) - 1

        xMargins: int = (sectorX + 1) * QUADRANT_MARGIN
        yMargins: int = (sectorY + 1) * QUADRANT_MARGIN

        x = (adjustSectorX * QUADRANT_PIXEL_WIDTH) + HALF_QUADRANT_PIXEL_WIDTH + xMargins
        y = (adjustSectorY * QUADRANT_PIXEL_HEIGHT) + HALF_QUADRANT_PIXEL_HEIGHT + yMargins + CONSOLE_HEIGHT

        return x, y
