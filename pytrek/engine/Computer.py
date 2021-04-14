
from typing import cast

from logging import Logger
from logging import getLogger

import math

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_MARGIN
from pytrek.Constants import QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_ROWS
from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates

from pytrek.Singleton import Singleton


class Computer(Singleton):
    """
    Make a computer a singleton so we don't have to pass it around
    """
    QUADRANT_TRAVEL_FACTOR: float = 0.1
    GALACTIC_TRAVEL_FACTOR: float = 1.0

    def init(self):

        #  self.settings = Settings()
        self.logger: Logger = getLogger(__name__)

    def computeSectorCoordinates(self, x: int, y: int) -> Coordinates:
        """
        From an arcade screen position determine which sector in quadrant
        """
        return self.computeCoordinates(x=x, y=y)

    def computeQuadrantCoordinates(self, x: int, y: int) -> Coordinates:
        return self.computeCoordinates(x=x, y=y)

    def computeCoordinates(self, x: int, y: int) -> Coordinates:

        adjustY: int = y - CONSOLE_HEIGHT

        gameX = int(math.floor(x // QUADRANT_PIXEL_WIDTH))
        gameY = int(math.floor(adjustY // QUADRANT_PIXEL_HEIGHT))

        adjustedGameY: int = (QUADRANT_ROWS - gameY) - 1

        coordinates = Coordinates(gameX, adjustedGameY)

        return coordinates

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

