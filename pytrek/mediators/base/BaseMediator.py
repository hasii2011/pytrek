
from logging import Logger
from logging import getLogger

from collections import namedtuple

from arcade import PointList
from arcade import Sound
from arcade import Sprite
from arcade import SpriteList

# noinspection PyPackageRequirements
from shapely.geometry import LineString
# noinspection PyPackageRequirements
from shapely.geometry import Polygon

from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer
from pytrek.gui.gamepieces.GamePiece import GamePiece

LineOfSightResponse = namedtuple('LineOfSightResponse', 'answer, obstacle')


class BaseMediator:

    clsLogger: Logger = getLogger(__name__)
    """
    Has common stuff to handle torpedo misses
    """
    def __init__(self):
        self._computer: Computer = Computer()

    @classmethod
    def loadSound(cls, bareFileName: str) -> Sound:

        fqFileName: str   = LocateResources.getResourcesPath(LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName)
        sound:      Sound = Sound(fqFileName)

        return sound

    def _pointAtTarget(self, shooter: Sprite, target: GamePiece, rotationAngle: int = 125):

        currentPoint:     ArcadePoint = ArcadePoint(x=shooter.center_x, y=shooter.center_y)
        destinationPoint: ArcadePoint = ArcadePoint(x=target.center_x,  y=target.center_y)

        normalAngle: float = self._computer.computeAngleToTarget(shooter=currentPoint, deadMeat=destinationPoint)
        shooter.angle = normalAngle + rotationAngle

        BaseMediator.clsLogger.info(f'{normalAngle=} -  {shooter.angle=}')

    def _hasLineOfSight(self, startingPoint: ArcadePoint, endPoint: ArcadePoint, obstacles: SpriteList) -> LineOfSightResponse:
        """
        This is my replacement for Arcade's has_line_of_sight();  The function is only returning a boolean and not the sprite
        or sprite's that are obstacles

        Args:
            startingPoint:
            endPoint:
            obstacles:

        Returns:  A LineOfSightResponse named tuple
        """
        lineOfSight: LineString = LineString([(startingPoint.x, startingPoint.y), (endPoint.x, endPoint.y)])

        for obstacle in obstacles:
            # obstacle: Sprite = cast(Sprite, obstacle)

            pointList: PointList = obstacle.get_adjusted_hit_box()
            polygon:   Polygon   = Polygon(pointList)
            ans: bool = polygon.crosses(lineOfSight)
            if ans is True:
                return LineOfSightResponse(answer=False, obstacle=obstacle)

        return LineOfSightResponse(answer=True, obstacle=None)
