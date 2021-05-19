
from typing import NewType
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from pytrek.Constants import GALAXY_COLUMNS
from pytrek.Constants import GALAXY_ROWS

from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings

from pytrek.GameState import GameState
from pytrek.Singleton import Singleton

QuadrantRow = NewType('QuadrantRow', List[Quadrant])
GalaxyGrid  = NewType('GalaxyGrid', List[QuadrantRow])


class Galaxy(Singleton):
    """
    Galaxy management
    """

    def init(self, *args, **kwds):
        """"""
        self._gameEngine:    GameEngine    = GameEngine()
        self._intelligence:  Intelligence  = Intelligence()
        self._gameState:    GameState     = GameState()
        self._gameSettings: GameSettings  = GameSettings()

        # self.stats          = GameState()
        # self.settings       = Settings()
        self.logger: Logger = getLogger(__name__)

        self.starBaseCount: int = 0
        self.planetCount:   int = 0
        self._currentQuadrant: Quadrant   = cast(Quadrant, None)
        self.quadrants:        GalaxyGrid = GalaxyGrid([])  # 2D array aka python list

        """
        For debugging purposes, collect a list of the coordinates where we placed Klingons;  
        There may be duplicate coordinates if we randomly picked the same quadrant
        """
        if self._gameSettings.debugCollectKlingonQuadrantCoordinates is True:
            self._debugKlingonQuadrants: List[Coordinates] = []
        self._createGalaxy()

        self.placeKlingonsInGalaxy()
        # self.placeCommandersInGalaxy()
        # self.placeStarBasesInGalaxy()
        self.setInitialQuadrant()

    def updateGalaxy(self):
        """"""

    def setInitialQuadrant(self):
        """"""
        coordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
        self.logger.info(f'Current Quadrant set to: {coordinates}')

        row: QuadrantRow = self.quadrants[coordinates.y]
        self._currentQuadrant = row[coordinates.x]

    @property
    def currentQuadrant(self) -> Quadrant:
        return self._currentQuadrant

    def placeKlingonsInGalaxy(self):
        """"""
        self.logger.info(f'Placing {self._gameState.remainingKlingons} Klingons')

        for x in range(self._gameState.remainingKlingons):

            coordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()

            if self._gameSettings.debugCollectKlingonQuadrantCoordinates is True:
                self._debugKlingonQuadrants.append(coordinates)

            quadrant: Quadrant = self.getQuadrant(coordinates)

            quadrant.addKlingon()

        if self._gameSettings.debugPrintKlingonPlacement is True:
            self._debugPrintKlingonPlacement()

    def placeCommandersInGalaxy(self):
        """"""
        # for x in range(self.stats.remainingCommanders):
        #     coordinates = self._intelligence.getRandomQuadrantCoordinates()
        #     quadrant    = self.getQuadrant(coordinates)
        #     quadrant.addCommander()
        pass

    def placeStarBasesInGalaxy(self):
        """"""
        # starBaseCount = self._intelligence.getInitialStarBaseCount()
        # while starBaseCount != 0:
        #     quadrantCoordinates = self._intelligence.getRandomQuadrantCoordinates()
        #     quadrant            = self.getQuadrant(quadrantCoordinates)
        #     while quadrant.hasStarBase() is True:
        #         quadrantCoordinates = self._intelligence.getRandomQuadrantCoordinates()
        #         quadrant = self.getQuadrant(quadrantCoordinates)
        #
        #     self.logger.debug(f"Starbase at quadrant {quadrantCoordinates}")
        #     quadrant.addStarBase()
        #     starBaseCount -= 1
        pass

    def getQuadrant(self, quadrantCoordinates: Coordinates) -> Quadrant:

        quadrantRow: QuadrantRow = self.quadrants[quadrantCoordinates.y]
        quadrant:    Quadrant    = quadrantRow[quadrantCoordinates.x]

        return quadrant

    def _createGalaxy(self):

        self.quadrants = []
        for y in range(GALAXY_ROWS):
            quadrantRow: QuadrantRow = QuadrantRow([])
            for x in range(GALAXY_COLUMNS):
                coordinates = Coordinates(x, y)
                quadrant = Quadrant(coordinates)
                quadrantRow.append(quadrant)
                if self._gameSettings.debugAnnounceQuadrantCreation is True:
                    self.logger.info(f"Created quadrant: ({x},{y})")
            self.quadrants.append(quadrantRow)

    def _debugPrintKlingonPlacement(self):
        """
        """
        for y in range(GALAXY_ROWS):
            quadRow = self.quadrants[y]
            for x in range(GALAXY_COLUMNS):
                quadrant = quadRow[x]
                quadrant: Quadrant = cast(Quadrant, quadrant)
                self.logger.info(f'Quadrant({x},{y}) Klingon Count: {quadrant.klingonCount}')
