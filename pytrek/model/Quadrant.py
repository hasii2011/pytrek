from logging import Logger
from logging import getLogger
from typing import List
from typing import NewType
from typing import cast

from arcade import Sprite

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS
from pytrek.Enterprise import Enterprise
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

        self._enterprise:            Enterprise  = cast(Enterprise, None)
        self._enterpriseCoordinates: Coordinates = cast(Coordinates, None)

        self._createQuadrant()

    def placeEnterprise(self, enterprise: Enterprise, coordinates: Coordinates):
        """

        Args:
            enterprise:     The fighting ship to place in this quadrant

            coordinates:    The sector coordinates in which to place the Enterprise
        """
        if self._enterpriseCoordinates is not None:

            oldEnterpriseRow = self._sectors[coordinates.y]
            oldSector = oldEnterpriseRow[self._enterpriseCoordinates.x]
            oldSector.setType(SectorType.EMPTY)
            oldSector.sprite = None

        self.logger.debug(f"Placing enterprise @quadrant: {coordinates}")

        sectorRow: SectorRow = self._sectors[coordinates.y]
        sector: Sector = sectorRow[coordinates.x]

        sector.type        = SectorType.ENTERPRISE
        sector.coordinates = coordinates
        sector.sprite = enterprise

        self.logger.info(f"Enterprise @sector: {coordinates}")

        self._enterprise = enterprise
        enterprise.currentPosition = coordinates
        self._enterpriseCoordinates = coordinates

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

    def _createQuadrant(self):
        for y in range(QUADRANT_ROWS):
            row: List[Sector] = []
            for x in range(QUADRANT_COLUMNS):

                coordinates: Coordinates = Coordinates(x=x, y=y)
                sector: Sector = Sector(sprite=cast(Sprite, None), type=SectorType.EMPTY, coordinates=coordinates)
                row.append(sector)
                self.logger.debug(f'Created empty sector ({x},{y})')
            self._sectors.append(row)
