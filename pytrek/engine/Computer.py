

from logging import Logger
from logging import getLogger

from math import atan2
from math import degrees
from math import fabs
from math import floor
from math import sin
from math import sqrt


from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import HALF_QUADRANT_PIXEL_WIDTH

from pytrek.Constants import QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_ROWS

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Intelligence import Intelligence

from pytrek.model.Coordinates import Coordinates

from pytrek.Singleton import Singleton


class Computer(Singleton):
    """
    Make a computer a singleton so we don't have to pass it around
    """
    QUADRANT_TRAVEL_FACTOR: float = 0.1
    GALACTIC_TRAVEL_FACTOR: float = 1.0

    def init(self):
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
        y = (adjustSectorY * QUADRANT_PIXEL_HEIGHT) + HALF_QUADRANT_PIXEL_HEIGHT + yMargins + CONSOLE_HEIGHT

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

        adjustY: float = y - CONSOLE_HEIGHT

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

        Returns:  A string in the from NNN
        """

        klingonCount = klingonCount + commanderCount
        quadrantValue = klingonCount * 100
        if hasStarBase:
            quadrantValue += 10

        strValue = str(quadrantValue).rjust(3, '0')

        return strValue

    def computeHitValueOnEnterprise(self, enemyPosition: Coordinates, enterprisePosition: Coordinates, enemyPower: float) -> float:
        """
        TODO: Move this to GameEngine
        Based on the Klingon power value and the distance between the two

        Args:
            enemyPosition:
            enterprisePosition:
            enemyPower:

        Returns:  The effective energy drainage on the Enterprise
        """

        distance:  float = self.computeQuadrantDistance(startSector=enemyPosition, endSector=enterprisePosition)
        hitFactor: float = 1.3 - distance
        hit:       float = enemyPower * hitFactor
        return hit

    def computeHitValueOnKlingon(self, enterprisePosition: Coordinates, klingonPosition: Coordinates, klingonPower: float) -> float:
        # noinspection SpellCheckingInspection
        """
        TODO: Move this to GameEngine

            bullseye = (15.0 - course)*0.5235988;
            r = (rand() + rand()) * 0.5 - 0.5;
            r += 0.002*game.kpower[loop]*r;

            ac=course + 0.25*r;
            angle = (15.0-ac)*0.5235988;
            inx, iny are game coordinates of the Enterprise

            h1 = 700.0 + 100.0*Rand() - 1000.0 * sqrt(square(ix-inx)+square(iy-iny)) * fabs(sin(bullseye-angle));
            h1 = fabs(h1);

        Args:
            enterprisePosition:
            klingonPosition:
            klingonPower:

        Returns  A computed answer based on the old SST `C` code
        """
        inx: int = enterprisePosition.x
        iny: int = enterprisePosition.y
        ix: int  = klingonPosition.x
        iy: int  = klingonPosition.y

        squaredX: float = self._intelligence.square(ix-inx)
        squaredY: float = self._intelligence.square(iy-iny)
        distance: float = sqrt(squaredX + squaredY)

        course:   float = self._computeCourse(start=enterprisePosition, end=klingonPosition)
        bullsEye: float = (15.0 - course) * 0.5235988
        r:        float = self._intelligence.rand() * self._intelligence.rand() * 0.5 - 0.5
        r = r + 0.002 * klingonPower * r

        ac:    float = course + 0.25 * r
        angle: float = (15.0 - ac) * 0.5235988

        h1: float = 700.0 + 100.0 * self._intelligence.rand() - 1000.0 * distance * fabs(sin(bullsEye - angle))

        return fabs(h1)

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

    def _computeCourse(self, start: Coordinates, end: Coordinates) -> float:
        # noinspection SpellCheckingInspection
        """
        These were original calculations;   Mine seem more correct.

        course = 1.90985932*atan2(deltaX, deltaY);

        double course = 1.90985 * atan2((double)secty-jy, (double)jx-sectx);

        Args:
            start: Start coordinates
            end:   Target coordinates

        Returns:  A game course in radians
        """

        deltaX: int = end.x - start.x
        deltaY: int = end.y - start.y
        course: float = atan2(deltaY, deltaX)

        return course
