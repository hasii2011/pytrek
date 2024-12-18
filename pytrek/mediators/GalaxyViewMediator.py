
from logging import Logger
from logging import getLogger

from arcade import color
from arcade import draw_text

from codeallybasic.SingletonV3 import SingletonV3

from pytrek.Constants import GALAXY_COLUMNS
from pytrek.Constants import GALAXY_ROWS
from pytrek.Constants import SUPER_NOVA_INDICATOR

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

SUPER_NOVA_X_ADJUSTMENT: int = 10


class GalaxyViewMediator(metaclass=SingletonV3):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._computer: Computer = Computer()
        self._galaxy:   Galaxy   = Galaxy()

    def draw(self, centerCoordinates: Coordinates):

        for y in range(GALAXY_ROWS):
            for x in range(GALAXY_COLUMNS):
                coordinates: Coordinates = Coordinates(x=x, y=y)
                quadrant: Quadrant = self._galaxy.getQuadrant(quadrantCoordinates=coordinates)

                if quadrant.scanned is True:
                    if centerCoordinates == coordinates:
                        contents: str = 'E'
                        arcadePoint: ArcadePoint = Computer.gamePositionToScreenPoint(coordinates)
                        arcadeX: float = arcadePoint.x + 2
                        arcadeY: float = arcadePoint.y + 2
                    else:
                        if quadrant.hasSuperNova is True:
                            contents = SUPER_NOVA_INDICATOR
                        else:
                            contents = self._computer.createValueString(klingonCount=quadrant.klingonCount,
                                                                        commanderCount=quadrant.commanderCount,
                                                                        hasStarBase=quadrant.hasStarBase)

                        arcadePoint = Computer.gamePositionToScreenPoint(coordinates)
                        arcadeX = arcadePoint.x
                        arcadeY = arcadePoint.y

                        if contents == SUPER_NOVA_INDICATOR:
                            arcadeX -= SUPER_NOVA_X_ADJUSTMENT

                    draw_text(contents, arcadeX, arcadeY, color.WHITE, 14)
