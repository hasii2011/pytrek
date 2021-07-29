
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
        self._gameEngine:   GameEngine    = GameEngine()
        self._intelligence: Intelligence  = Intelligence()
        self._gameState:    GameState     = GameState()
        self._gameSettings: GameSettings  = GameSettings()

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

        # TODO  Debug option for No Klingon, No commanders, No Super Commanders
        self.placeKlingonsInGalaxy()
        self.placeCommandersInGalaxy()
        self.placeSuperCommandersInGalaxy()

        # self.placeStarBasesInGalaxy()
        self._placePlanets()
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
        """
        """
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
        """
        """
        for x in range(self._gameState.remainingCommanders):
            coordinates = self._intelligence.generateQuadrantCoordinates()
            quadrant    = self.getQuadrant(coordinates)
            quadrant.addCommander()

    def placeSuperCommandersInGalaxy(self):
        """
        """
        for x in range(self._gameState.remainingSuperCommanders):
            coordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
            # if self._gameSettings.debugCollectSuperCommanderQuadrantCoordinates is True:
            #     self._debugSuperCommanderQuadrants.append(coordinates)
            quadrant    = self.getQuadrant(coordinates)
            quadrant.addSuperCommander()

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
        #     self.logger.debug(f"StarBase at quadrant {quadrantCoordinates}")
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

    # noinspection SpellCheckingInspection
    def _placePlanets(self):
        """
        ```java
            for (int i = 0; i < myPlanetCount; i++) {

                Coordinates pCoords = Intelligence.getRandomQuadrantCoordinates();
                int         x       = pCoords.getXCoordinate();
                int         y       = pCoords.getYCoordinate();
                Quadrant    pQuad   = myQuadrants[x][y];
                pQuad.addPlanet();
            }
        ```
        """
        planetCount: int = self._intelligence.computePlanetsInGalaxy()
        for x in range(planetCount):

            quadrantCoordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
            quadrant:            Quadrant    = self.getQuadrant(quadrantCoordinates)
            #
            # Quadrants are allowed only a single planet and cannot have a starbase
            #
            while quadrant.hasPlanet is True or quadrant.hasStarBase is True:
                quadrantCoordinates = self._intelligence.generateQuadrantCoordinates()
                quadrant            = self.getQuadrant(quadrantCoordinates)
                self.logger.warning(f'Generated new quadrant for planet')

            quadrant.addPlanet()
            self.logger.info(f'Quadrant: {quadrantCoordinates} has a planet')

    def _debugPrintKlingonPlacement(self):
        """
        """
        for y in range(GALAXY_ROWS):
            quadRow = self.quadrants[y]
            for x in range(GALAXY_COLUMNS):
                quadrant = quadRow[x]
                quadrant: Quadrant = cast(Quadrant, quadrant)
                self.logger.info(f'Quadrant({x},{y}) Klingon Count: {quadrant.klingonCount}')
