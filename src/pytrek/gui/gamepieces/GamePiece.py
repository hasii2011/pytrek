
from pytrek.Constants import HALF_QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_ROWS
from pytrek.Constants import QUADRANT_Y_ADJUSTMENT

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.base.BaseGamePiece import BaseGamePiece

from pytrek.model.Coordinates import Coordinates


class GamePiece(BaseGamePiece):

    def __init__(self, filename: str = '', speed: float = 2, scale: float = 1.0):

        super().__init__(filename=filename, scale=scale)

        self._speed: float = speed
        """
        Max speed
        """
        self._rotationSpeed: float = 3
        """
        Max speed we can rotate
        """

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
    def gamePositionToScreenPosition(cls, gameCoordinates: Coordinates) -> ArcadePoint:

        sectorX: int = gameCoordinates.x
        sectorY: int = gameCoordinates.y
        #
        # because game coordinates are top L - R and down
        # and game coordinates are 0-based
        adjustSectorX: int = sectorX
        adjustSectorY: int = (QUADRANT_ROWS - sectorY) - 1

        x = (adjustSectorX * QUADRANT_PIXEL_WIDTH) + HALF_QUADRANT_PIXEL_WIDTH
        y = (adjustSectorY * QUADRANT_PIXEL_HEIGHT) + HALF_QUADRANT_PIXEL_HEIGHT + QUADRANT_Y_ADJUSTMENT

        arcadePoint: ArcadePoint = ArcadePoint(x=x, y=y)
        return arcadePoint
