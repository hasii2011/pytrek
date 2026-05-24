from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from arcade import color
from arcade import Text

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

QUADRANT_SECTORS = NewType('QUADRANT_SECTORS', List[Text])
GALAXY_GRID      = NewType('GALAXY_GRID', List[QUADRANT_SECTORS])


class GalaxyViewMediator(metaclass=SingletonV3):
    """
    This class is responsible for rendering the Galaxy Map overlay.

    It coordinates drawing scanned quadrants in the galaxy grid by mapping
    each quadrant to its corresponding screen coordinates and displaying its contents
    (such as the player's current location, supernova indicators, or scanned stellar objects).

    Design & Performance Optimizations:
    - Pre-allocates a 8x8 grid of cached `arcade.Text` objects during initialization.
    - Updates text values and coordinates
    - Renders the cached text objects dynamically

    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._computer: Computer = Computer()
        self._galaxy:   Galaxy   = Galaxy()

        self._quadrantGrid: GALAXY_GRID = self._initializeGalaxyTextGrid()

    def draw(self, centerCoordinates: Coordinates):

        for y in range(GALAXY_ROWS):
            for x in range(GALAXY_COLUMNS):
                coordinates: Coordinates = Coordinates(x=x, y=y)
                quadrant: Quadrant = self._galaxy.getQuadrant(quadrantCoordinates=coordinates)

                if quadrant.scanned:
                    quadrantContents = self._quadrantGrid[y][x]
                    if centerCoordinates == coordinates:
                        arcadePoint: ArcadePoint = Computer.gamePositionToScreenPoint(coordinates)
                        arcadeX: float = arcadePoint.x + 2
                        arcadeY: float = arcadePoint.y + 2
                        quadrantContents.text = 'E'
                    else:
                        if quadrant.hasSuperNova:
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

                        quadrantContents.text = contents

                    quadrantContents.x = arcadeX
                    quadrantContents.y = arcadeY

                    quadrantContents.draw()

    def _initializeGalaxyTextGrid(self)-> GALAXY_GRID:
        """
        One time initialization of arcade Text objects

        Returns:  The quadrant grid

        """
        quadrantGrid: GALAXY_GRID = GALAXY_GRID([QUADRANT_SECTORS([])])

        for y in range(GALAXY_ROWS):
            row: QUADRANT_SECTORS = QUADRANT_SECTORS([])
            for x in range(GALAXY_COLUMNS):
                coordinates = Coordinates(x=x, y=y)
                arcadePoint = Computer.gamePositionToScreenPoint(coordinates)

                quadrantContents: Text = Text(
                    text='',
                    x=arcadePoint.x,
                    y=arcadePoint.y,
                    color=color.WHITE,
                    font_size=14
                )
                row.append(quadrantContents)
            quadrantGrid.append(row)

        return quadrantGrid
