
from logging import Logger
from logging import getLogger

from arcade import color
from arcade import draw_text

from pytrek.Constants import GALAXY_COLUMNS
from pytrek.Constants import GALAXY_ROWS

from pytrek.Singleton import Singleton

from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.engine.Computer import Computer

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant


class GalaxyViewMediator(Singleton):

    def init(self, *args, **kwds):

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
                        arcadePosition: ArcadePosition = Computer.gamePositionToScreenPosition(coordinates)
                        arcadeX: float = arcadePosition.x + 2
                        arcadeY: float = arcadePosition.y + 2
                    else:
                        contents = self._computer.createValueString(klingonCount=quadrant.klingonCount,
                                                                    commanderCount=quadrant.commanderCount,
                                                                    hasStarBase=quadrant.hasStarBase)

                        arcadePosition = Computer.gamePositionToScreenPosition(coordinates)
                        arcadeX = arcadePosition.x
                        arcadeY = arcadePosition.y

                    draw_text(contents, arcadeX, arcadeY, color.WHITE, 14)
