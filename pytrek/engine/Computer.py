

from logging import Logger
from logging import getLogger

import math

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_WIDTH

from pytrek.Constants import QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_ROWS
from pytrek.engine.ArcadePosition import ArcadePosition

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

    @classmethod
    def gamePositionToScreenPosition(cls, gameCoordinates: Coordinates) -> ArcadePosition:
        """
        Computes x,y arcade position within the galaxy
        Args:
            gameCoordinates:   The game coordinates

        Returns:  Arcade x,y Position

        """

        sectorX: int = gameCoordinates.x
        sectorY: int = gameCoordinates.y
        #
        # because game coordinates are top L - R and down
        # and game coordinates are 0-based
        adjustSectorX: int = sectorX
        adjustSectorY: int = (QUADRANT_ROWS - sectorY) - 1

        xMargins = -12  # Font Fudge Factor
        yMargins = -12  # Font Fudge Factor

        x = (adjustSectorX * QUADRANT_PIXEL_WIDTH) + HALF_QUADRANT_PIXEL_WIDTH + xMargins
        y = (adjustSectorY * QUADRANT_PIXEL_HEIGHT) + HALF_QUADRANT_PIXEL_HEIGHT + yMargins + CONSOLE_HEIGHT

        return ArcadePosition(x=x, y=y)

    def computeSectorCoordinates(self, x: float, y: float) -> Coordinates:
        """
        From an arcade screen point determine which sector in quadrant

        Args:
            x: Arcade X
            y: Arcade Y

        Returns:  Game Sector Coordinates
        """
        return self.computeCoordinates(x=x, y=y)

    def computeQuadrantCoordinates(self, x: float, y: float) -> Coordinates:
        return self.computeCoordinates(x=x, y=y)

    def computeCoordinates(self, x: float, y: float) -> Coordinates:

        adjustY: float = y - CONSOLE_HEIGHT

        gameX = int(math.floor(x // QUADRANT_PIXEL_WIDTH))
        gameY = int(math.floor(adjustY // QUADRANT_PIXEL_HEIGHT))

        adjustedGameY: int = (QUADRANT_ROWS - gameY) - 1

        coordinates = Coordinates(gameX, adjustedGameY)

        return coordinates

    def computeQuadrantDistance(self, startSector: Coordinates, endSector: Coordinates) -> float:
        """

        Args:
            startSector:
            endSector:

        Returns:
        """
        return self._computeDistance(startSector, endSector, Computer.QUADRANT_TRAVEL_FACTOR)

    def createValueString(self, klingonCount: int, commanderCount: int, hasStarBase: bool) -> str:
        """
        Turn the input parameters into a numeric string that can be used to display
        as the contents of a quadrant either in the Galaxy View or a long range sensor scan
        Args:
            klingonCount:   The Quadrant's klingon count
            commanderCount: The Quadrant's commander count
            hasStarBase:    Indicates whether the quadrant has a star bae

        Returns:  A string in the from NNN
        """

        klingonCount = klingonCount + commanderCount
        quadrantValue = klingonCount * 100
        if hasStarBase:
            quadrantValue += 10

        strValue = str(quadrantValue).rjust(3, '0')

        return strValue

    def _computeDistance(self, startCoordinates: Coordinates, endCoordinates: Coordinates, travelFactor: float) -> float:
        """
        From Java code:
        ```java
         x1 = startSector.getX()
         y1 = startSector.getY()
         x2 = endSector.getX()
         y2 = endSector.getY()

         deltaX = x2 - x1
         deltaY = y2 - y1

         distance = travelFactor * math.sqrt( (deltaX * deltaX) + (deltaY * deltaY) )
        ```
        Args:
            startCoordinates:
            endCoordinates:
            travelFactor:  accounts for quadrant travel or galactic travel

        Returns:    The game distance between the above
        """

        x1 = startCoordinates.x
        y1 = startCoordinates.y
        x2 = endCoordinates.x
        y2 = endCoordinates.y

        self.logger.debug(f"{x1=} {y1=} {x2=} {y2=}")

        deltaX = x2 - x1
        deltaY = y2 - y1
        self.logger.debug(f"{deltaX=} {deltaY=}")

        distance = travelFactor * math.sqrt((deltaX * deltaX) + (deltaY * deltaY))

        self.logger.debug(f"Quadrant Distance: {distance}")

        return distance
