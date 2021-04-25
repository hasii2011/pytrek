from logging import Logger
from logging import getLogger
from typing import List
from typing import NewType
from typing import cast

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS

from pytrek.engine.Intelligence import Intelligence


from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.Klingon import Klingon

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType


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

        self._klingonCount:   int = 0
        self._commanderCount: int = 0

        self._klingons:   List[Klingon]   = []
        # self.commanders: List[Commander] = []

        self._enterprise:            Enterprise  = cast(Enterprise, None)
        self._enterpriseCoordinates: Coordinates = cast(Coordinates, None)

        self._createQuadrant()

    def placeEnterprise(self, enterprise: Enterprise, coordinates: Coordinates):
        """
        Explicitly place the Enterprise;   Since only one it is possible to have doppelganger Enterprises'
        from alternate timelines;  Hopefully, not woke timelines.

        Args:
            enterprise:     The fighting ship to place in this quadrant

            coordinates:    The sector coordinates in which to place the Enterprise
        """
        if self._enterpriseCoordinates is not None:

            oldEnterpriseRow = self._sectors[coordinates.y]
            oldSector = oldEnterpriseRow[self._enterpriseCoordinates.x]
            oldSector.type = SectorType.EMPTY
            oldSector.sprite = None

        self.logger.debug(f"Placing enterprise @quadrant: {coordinates}")

        sectorRow: SectorRow = self._sectors[coordinates.y]
        sector: Sector = sectorRow[coordinates.x]

        sector.type        = SectorType.ENTERPRISE
        sector.coordinates = coordinates
        sector.sprite      = enterprise

        self.logger.info(f"Enterprise @sector: {coordinates}")

        self._enterprise = enterprise
        enterprise.currentPosition  = coordinates
        self._enterpriseCoordinates = coordinates

    @property
    def coordinates(self) -> Coordinates:
        """
        Read-only as set when the quadrant is created

        Returns:  Our coordinates in the Galaxy
        """
        return self._coordinates

    @property
    def enterprise(self) -> Enterprise:
        """
        Read only property as we cannot have doppelganger Enterprises from other timelines !!!

        Returns:  The Enterprise Sprite
        """
        return self._enterprise

    @property
    def enterpriseCoordinates(self):
        return self._enterpriseCoordinates

    @enterpriseCoordinates.setter
    def enterpriseCoordinates(self, newCoordinates: Coordinates):
        self._enterpriseCoordinates = newCoordinates

    @property
    def klingonCount(self):
        """"""
        return self._klingonCount

    @property
    def klingons(self) -> List[Klingon]:
        return self._klingons

    def getSector(self, sectorCoordinates: Coordinates) -> Sector:
        """

        Args:
            sectorCoordinates:

        Returns:  The sector at x,y

        """
        sectorRow: SectorRow = self._sectors[sectorCoordinates.y]
        sector:    Sector    = sectorRow[sectorCoordinates.x]

        return sector

    def addKlingon(self):
        """"""
        self._klingonCount += 1
        klingon = self.placeAKlingon()
        self._klingons.append(klingon)

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

    def placeAKlingon(self) -> Klingon:
        """

        """
        sector      = self.getRandomEmptySector()
        sector.type = SectorType.KLINGON
        klingon     = Klingon(coordinates=sector.coordinates)
        kPower      = self._intelligence.computeKlingonPower()

        klingon.power = kPower
        sector.sprite = klingon

        self.logger.debug(f"Placed klingon at: quadrant: {self._coordinates} {sector=}, {kPower=}")
        return klingon

    def _createQuadrant(self):
        for y in range(QUADRANT_ROWS):
            row: List[Sector] = []
            for x in range(QUADRANT_COLUMNS):

                coordinates: Coordinates = Coordinates(x=x, y=y)
                sector: Sector = Sector(sprite=cast(GamePiece, None), type=SectorType.EMPTY, coordinates=coordinates)
                row.append(sector)
                self.logger.debug(f'Created empty sector ({x},{y})')
            self._sectors.append(row)
