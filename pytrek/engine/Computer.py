
from logging import Logger
from logging import getLogger

from codeallybasic.SingletonV3 import SingletonV3

from math import atan2
from math import degrees
from math import floor
from math import sqrt


from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_WIDTH

from pytrek.Constants import QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_ROWS

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Intelligence import Intelligence

from pytrek.model.Coordinates import Coordinates


class Computer(metaclass=SingletonV3):
    """
    Make a computer a singleton, so we don't have to pass it around
    Makes basic computations related to converting to and from game coordinates
    and the underlying PyArcade point system;
    This unrelated to the game 'computer'
    """
    QUADRANT_TRAVEL_FACTOR: float = 0.1
    GALACTIC_TRAVEL_FACTOR: float = 10.0

    def __init__(self):
        self.logger:        Logger       = getLogger(__name__)
        self._intelligence: Intelligence = Intelligence()

    @classmethod
    def gamePositionToScreenPoint(cls, gameCoordinates: Coordinates) -> ArcadePoint:
        """
        This is strictly for the GameView;  GamePieces need to use GamePiece.gamePositionToScreenPosition
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
        y = (adjustSectorY * QUADRANT_PIXEL_HEIGHT) + HALF_QUADRANT_PIXEL_HEIGHT + yMargins + CONSOLE_SECTION_HEIGHT

        return ArcadePoint(x=x, y=y)

    @classmethod
    def computeCenterPoint(cls, start: ArcadePoint, end: ArcadePoint) -> ArcadePoint:

        x1: float = start.x
        x2: float = end.x
        y1: float = start.y
        y2: float = end.y

        midX: float = (x1 + x2) // 2
        midY: float = (y1 + y2) // 2

        return ArcadePoint(x=midX, y=midY)

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

        adjustY: float = y - CONSOLE_SECTION_HEIGHT

        gameX = int(floor(x // QUADRANT_PIXEL_WIDTH))
        gameY = int(floor(adjustY // QUADRANT_PIXEL_HEIGHT))

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

    def computeGalacticDistance(self, startQuadrantCoordinates: Coordinates, endQuadrantCoordinates: Coordinates) -> float:
        """"""
        return self._computeDistance(startQuadrantCoordinates, endQuadrantCoordinates, Computer.GALACTIC_TRAVEL_FACTOR)

    def createValueString(self, klingonCount: int, commanderCount: int, hasStarBase: bool) -> str:
        """
        Turn the input parameters into a numeric string that can be used to display
        as the contents of a quadrant either in the Galaxy View or a long range sensor scan
        Args:
            klingonCount:   The Quadrant's klingon count
            commanderCount: The Quadrant's commander count
            hasStarBase:    Indicates whether the quadrant has a star bae

        Returns:  A string in the form NNN
        """

        klingonCount = klingonCount + commanderCount
        quadrantValue = klingonCount * 100
        if hasStarBase:
            quadrantValue += 10

        strValue = str(quadrantValue).rjust(3, '0')

        return strValue

    def computeAngleToTarget(self, shooter: ArcadePoint, deadMeat: ArcadePoint) -> float:
        """
        x goes right (as expected)
        y goes up
        Adjust degrees since we use Arcade's coordinate system

        Args:
            shooter:
            deadMeat:

        Returns:  correct angle in degrees

        """

        deltaX: float = deadMeat.x - shooter.x
        deltaY: float = deadMeat.y - shooter.y

        angleRadians: float = atan2(deltaY, deltaX)
        angleDegrees: float = degrees(angleRadians)

        return angleDegrees

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

        x1: int = startCoordinates.x
        y1: int = startCoordinates.y
        x2: int = endCoordinates.x
        y2: int = endCoordinates.y

        self.logger.debug(f"{x1=} {y1=} {x2=} {y2=}")

        deltaX: int = x2 - x1
        deltaY: int = y2 - y1
        self.logger.debug(f"{deltaX=} {deltaY=}")

        distance: float = travelFactor * sqrt((deltaX * deltaX) + (deltaY * deltaY))

        self.logger.debug(f"{distance=}")

        return distance
