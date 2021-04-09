
from typing import cast

from arcade import Sprite

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import QUADRANT_MARGIN
from pytrek.Constants import QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_ROWS

from pytrek.model.Coordinates import Coordinates

HALF_QUADRANT_PIXEL_WIDTH:  int = QUADRANT_PIXEL_WIDTH // 2
HALF_QUADRANT_PIXEL_HEIGHT: int = QUADRANT_PIXEL_HEIGHT // 2


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
