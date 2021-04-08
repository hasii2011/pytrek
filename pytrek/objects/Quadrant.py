from logging import Logger
from logging import getLogger
from typing import List
from typing import NewType
from typing import cast

from arcade import Sprite

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS
from pytrek.engine.Intelligence import Intelligence
from pytrek.objects.Coordinates import Coordinates
from pytrek.objects.Sector import Sector
from pytrek.objects.SectorType import SectorType


SectorRow    = NewType('SectorRow', List[Sector])
QuadrantGrid = NewType('GalaxyGrid', List[SectorRow])


class Quadrant:

    """
    Quadrant Management
    """
    def __init__(self, coordinates: Coordinates):
        """
            Initialize a quadrant
        """
        self.logger:       Logger       = getLogger(__name__)
        self._coordinates: Coordinates  = coordinates
        self._sectors:     QuadrantGrid = QuadrantGrid([])

        self._intelligence: Intelligence = Intelligence()

        for y in range(QUADRANT_ROWS):
            row: List[Sector] = []
            for x in range(QUADRANT_COLUMNS):

                coordinates: Coordinates = Coordinates(x=x, y=y)
                sector: Sector = Sector(sprite=cast(Sprite, None), type=SectorType.EMPTY, coordinates=coordinates)
                row.append(sector)
                self.logger.debug(f'Created empty sector ({x},{y})')
            self._sectors.append(row)

    def placeEnterprise(self):
        pass

    def getSector(self, sectorCoordinates: Coordinates) -> Sector:
        """

        Args:
            sectorCoordinates:

        Returns:  The sector at x,y

        """
        sectorRow: SectorRow = self._sectors[sectorCoordinates.y]
        sector:    Sector    = sectorRow[sectorCoordinates.x]

        return sector

    def getRandomEmptySector(self) -> Sector:
        """

        Returns:  An empty sector
        """

        randomSectorCoordinates = self._intelligence.generateSectorCoordinates()
        sector                  = self.getSector(randomSectorCoordinates)

        while sector.type != SectorType.EMPTY:
            randomSectorCoordinates = self._intelligence.generateSectorCoordinates()
            sector = self.getSector(randomSectorCoordinates)

        return sector
