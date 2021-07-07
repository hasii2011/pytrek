
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS

from pytrek.gui.gamepieces.commander.Commander import Commander
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.gui.gamepieces.GamePieceTypes import Enemy

from pytrek.gui.gamepieces.klingon.Klingon import Klingon
from pytrek.gui.gamepieces.Planet import Planet
from pytrek.gui.gamepieces.PlanetType import PlanetType
from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.engine.Intelligence import Intelligence

from pytrek.settings.GameSettings import GameSettings

SectorRow    = NewType('SectorRow', List[Sector])
QuadrantGrid = NewType('QuadrantGrid', List[SectorRow])


class Quadrant:

    """
    Quadrant Management
    """
    def __init__(self, coordinates: Coordinates):
        """
            Initialize a quadrant
        """
        from pytrek.engine.GameEngine import GameEngine     # Avoid recursion

        self.logger:       Logger       = getLogger(__name__)
        self._coordinates: Coordinates  = coordinates
        self._sectors:     QuadrantGrid = QuadrantGrid([])

        self._intelligence: Intelligence = Intelligence()
        self._gameEngine:   GameEngine   = GameEngine()
        self._gameSettings: GameSettings = GameSettings()

        self._klingonCount:        int = 0
        self._commanderCount:      int = 0
        self._superCommanderCount: int = 0
        self._hasStarBase:    bool = False
        self._hasPlanet:      bool = False
        self._scanned:        bool = False

        self._klingons:        Enemies = Enemies([])
        self._commanders:      Enemies = Enemies([])
        self._superCommanders: Enemies = Enemies([])

        self._planet: Planet = cast(Planet, None)

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
            oldSector: Sector = oldEnterpriseRow[self._enterpriseCoordinates.x]
            oldSector.type = SectorType.EMPTY
            oldSector.sprite = cast(GamePiece, None)

        self.logger.debug(f"Placing enterprise @quadrant: {coordinates}")

        sectorRow: SectorRow = self._sectors[coordinates.y]
        sector: Sector = sectorRow[coordinates.x]

        sector.type        = SectorType.ENTERPRISE
        sector.coordinates = coordinates
        sector.sprite      = enterprise

        self.logger.info(f"Enterprise @sector: {coordinates}")

        self._enterprise = enterprise
        enterprise.gameCoordinates  = coordinates
        self._enterpriseCoordinates = coordinates
        self.scanned = True     # Naturally, we are here

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
    def commanderCount(self) -> int:
        return self._commanderCount

    @commanderCount.setter
    def commanderCount(self, newValue: int):
        self._commanderCount = newValue

    @property
    def superCommanderCount(self) -> int:
        return self._superCommanderCount

    @superCommanderCount.setter
    def superCommanderCount(self, newValue: int):
        self._superCommanderCount = newValue

    @property
    def klingons(self) -> Enemies:
        return self._klingons

    @property
    def commanders(self) -> Enemies:
        return self._commanders

    @property
    def superCommanders(self) -> Enemies:
        return self._superCommanders

    @property
    def scanned(self) -> bool:
        """
        Returns whether or not this quadrant was part of a long range sensor scan

        Returns:  `True` if this quadrant participated in a long range sensor scan, else `False`
        """
        return self._scanned

    @scanned.setter
    def scanned(self, newValue: bool):
        self._scanned = newValue

    @property
    def hasStarBase(self) -> bool:
        return self._hasStarBase

    @hasStarBase.setter
    def hasStarBase(self, newValue: bool):
        self._hasStarBase = newValue

    @property
    def hasPlanet(self) -> bool:
        return self._hasPlanet

    @property
    def planet(self) -> Planet:
        return self._planet

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
        klingon: Klingon = self._placeAKlingon()
        self._klingons.append(klingon)

    def addCommander(self):
        """
        """
        self._commanderCount += 1
        commander: Commander = self._placeACommander()
        self._commanders.append(commander)

    def addSuperCommander(self):
        """
        """
        self._superCommanderCount += 1
        superCommander: SuperCommander = self._placeASuperCommander()
        
        self._superCommanders.append(superCommander)

    def addPlanet(self):

        self._hasPlanet = True

        sector      = self.getRandomEmptySector()
        sector.type = SectorType.PLANET

        planetType: PlanetType = self._intelligence.computeRandomPlanetType()
        self._planet = Planet(planetType=planetType, sectorCoordinates=sector.coordinates)

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

    def _placeAKlingon(self) -> Klingon:
        """
        Creates a enemy and places it at a random empty sector
        """

        sector        = self.getRandomEmptySector()
        sector.type   = SectorType.KLINGON

        moveInterval: int      = self._intelligence.computeKlingonMoveInterval()
        klingon     = Klingon(coordinates=sector.coordinates, moveInterval=moveInterval)

        klingon.power          = self._intelligence.computeKlingonPower()
        klingon.firingInterval = self._intelligence.computeKlingonFiringInterval()
        klingon.lastTimeCheck  = round(self._gameEngine.gameClock // 1000)

        sector.sprite = klingon

        if sector.coordinates.x == 0 and sector.coordinates.y == 0:
            print(f'{klingon.id=} is at sector: {sector.coordinates}')

        self.logger.debug(f"Placed enemy at quadrant: {self._coordinates} {klingon=}")
        return klingon

    def _placeACommander(self) -> Commander:
        """
        Create and place a Commander at a random empty sector

        Returns:  The 'placed" commander
        """
        sector      = self.getRandomEmptySector()
        sector.type = SectorType.COMMANDER

        moveInterval: int       = self._intelligence.computeCommanderMoveInterval()
        commander:    Commander = Commander(coordinates=sector.coordinates, moveInterval=moveInterval)
        cPower:       float     = self._intelligence.computeCommanderPower()

        commander.power = cPower
        commander.firingInterval    = self._intelligence.computeCommanderFiringInterval()
        commander.timeSinceMovement = self._gameEngine.gameClock

        sector.sprite = commander

        self.logger.debug(f'Placed commander at quadrant: {self.coordinates} {commander=}')
        return commander

    def _placeASuperCommander(self) -> SuperCommander:

        sector: Sector      = self.getRandomEmptySector()
        sector.type = SectorType.SUPER_COMMANDER

        moveInterval: int = self._intelligence.computeSuperCommanderMoveInterval()

        superCommander: SuperCommander = SuperCommander(coordinates=sector.coordinates, moveInterval=moveInterval)

        # scPower: float = self._intelligence.computeSuperCommanderPower()
        scPower: float = 800.0

        superCommander.power             = scPower
        superCommander.firingInterval    = 3  # TODO: call intelligence
        superCommander.timeSinceMovement = self._gameEngine.gameClock

        sector.sprite = superCommander
        return superCommander

    def removeDeadEnemies(self):

        self._klingons        = self._removeZombies(self._klingons)
        self._commanders      = self._removeZombies(self._commanders)
        self._superCommanders = self._removeZombies(self._superCommanders)

        # TODO:   Clean up Commanders and SuperCommanders

    def _removeZombies(self, enemies: Enemies):

        liveKlingons: Enemies = Enemies([])

        for zombie in enemies:
            enemy: Enemy = cast(Enemy, zombie)
            if enemy.power == 0:
                self.logger.info(f'Found dead enemy: {enemy.id}')
                self._klingonCount -= 1
                sector: Sector = self.getSector(enemy.gameCoordinates)
                sector.type = SectorType.EMPTY
            else:
                liveKlingons.append(enemy)

        return liveKlingons

    def _createQuadrant(self):
        for y in range(QUADRANT_ROWS):
            row: List[Sector] = []
            for x in range(QUADRANT_COLUMNS):

                coordinates: Coordinates = Coordinates(x=x, y=y)
                sector: Sector = Sector(sprite=cast(GamePiece, None), type=SectorType.EMPTY, coordinates=coordinates)
                row.append(sector)
                self.logger.debug(f'Created empty sector ({x},{y})')
            self._sectors.append(row)

    def __str__(self) -> str:

        depiction: str = (
            f'coordinates={self.coordinates} '
            f'klingonCount={self.klingonCount} '
            f'commanderCount={self.commanderCount} '
            f'hasStarBase={self.hasStarBase}'
        )

        return depiction

    def __repr__(self) -> str:
        return self.__str__()
