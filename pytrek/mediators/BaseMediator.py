
from typing import cast

from collections import namedtuple

from arcade import PointList
from arcade import Sprite
from arcade import SpriteList

# noinspection PyPackageRequirements
from shapely.geometry import LineString
# noinspection PyPackageRequirements
from shapely.geometry import Polygon

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.gui.MessageConsole import MessageConsole

from pytrek.GameState import GameState

LineOfSightResponse = namedtuple('LineOfSightResponse', 'answer, obstacle')


class BaseMediator:
    """
    Has common stuff that many mediators will need
    """
    def __init__(self):

        self._computer:       Computer       = Computer()
        self._gameState:      GameState      = GameState()
        self._gameEngine:     GameEngine     = GameEngine()
        self._intelligence:   Intelligence   = Intelligence()

        self._messageConsole: MessageConsole = MessageConsole()

    def hasLineOfSight(self, startingPoint: ArcadePoint, endPoint: ArcadePoint, obstacles: SpriteList) -> LineOfSightResponse:
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
            obstacle: Sprite = cast(Sprite, obstacle)

            pointList: PointList = obstacle.get_adjusted_hit_box()
            polygon:   Polygon   = Polygon(pointList)
            ans: bool = polygon.crosses(lineOfSight)
            if ans is True:
                return LineOfSightResponse(answer=False, obstacle=obstacle)

        return LineOfSightResponse(answer=True, obstacle=None)
