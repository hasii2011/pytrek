
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

    MAX_STARBASE_SEARCHES: int = 128

    def init(self, *args, **kwds):
        """"""
        self._gameEngine:   GameEngine    = GameEngine()
        self._intelligence: Intelligence  = Intelligence()
        self._gameState:    GameState     = GameState()
        self._gameSettings: GameSettings  = GameSettings()

        self.logger: Logger = getLogger(__name__)

        self._currentQuadrant: Quadrant   = cast(Quadrant, None)
        self.quadrants:        GalaxyGrid = GalaxyGrid([])  # 2D array aka python list

        self._createGalaxy()

        self._addEnemies()

        self._placeStarBasesInGalaxy()
        self._placePlanetsInGalaxy()
        self._setInitialQuadrant()

        print(f'Galaxy singleton initialized')

    def _addEnemies(self):

        gameSettings: GameSettings = self._gameSettings
        """
            For debugging purposes, collect a list of the coordinates where we placed Klingons;  
            There may be duplicate coordinates if we randomly picked the same quadrant
            """
        print(f'Galaxy: {gameSettings.debugCollectKlingonQuadrantCoordinates=}')
        if gameSettings.debugCollectKlingonQuadrantCoordinates is True:
            self._debugKlingonQuadrants: List[Coordinates] = []

        if gameSettings.debugNoKlingons is True:
            self._gameState.remainingKlingons = 0
        else:
            self.__placeKlingonsInGalaxy()
        if gameSettings.debugNoCommanders is True:
            self._gameState.remainingCommanders = 0
        else:
            self.__placeCommandersInGalaxy()
        if gameSettings.debugNoSuperCommanders is True:
            self._gameState.remainingSuperCommanders = 0
        else:
            self.__placeSuperCommandersInGalaxy()

    def updateGalaxy(self):
        """"""

    @property
    def currentQuadrant(self) -> Quadrant:
        return self._currentQuadrant

    @currentQuadrant.setter
    def currentQuadrant(self, quadrant: Quadrant):
        self._currentQuadrant = quadrant

    def getStarBaseCoordinates(self) -> Coordinates:
        """
        Randomly search the galaxy for a quadrant that has a star base.
        Loop trough MAX_STARBASE_SEARCHES;  If we cannot find one, perhaps
        there are no star bases;  Return None

        Returns:  The randomly located quadrant with a star base;  If no StarBases
        left return None
        """
        for x in range(Galaxy.MAX_STARBASE_SEARCHES):

            potentialCoordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
            quadrant:             Quadrant    = self.getQuadrant(quadrantCoordinates=potentialCoordinates)
            if quadrant.hasStarBase is True:
                # print(f'Executed {x} iterations to find 1 of  {self._gameState.starBaseCount} StarBases')
                return potentialCoordinates

        return cast(Coordinates, None)

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

    def _placePlanetsInGalaxy(self) -> int:
        # noinspection SpellCheckingInspection
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
        planetCount: int = self._gameState.planetCount
        for x in range(planetCount):

            quadrantCoordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
            quadrant:            Quadrant    = self.getQuadrant(quadrantCoordinates)
            #
            # Quadrants are allowed only a single planet and cannot have a starbase
            #
            while quadrant.hasPlanet is True or quadrant.hasStarBase is True:
                quadrantCoordinates = self._intelligence.generateQuadrantCoordinates()
                quadrant            = self.getQuadrant(quadrantCoordinates)
                self.logger.debug(f'Generated new quadrant for planet')

            quadrant.addPlanet()
            self.logger.info(f'Quadrant: {quadrantCoordinates} has a planet')

        return planetCount

    def _placeStarBasesInGalaxy(self):
        """
        Place a random number of bases in the galaxy

        """
        starBaseCount: int = self._gameState.starBaseCount
        while starBaseCount != 0:
            quadrantCoordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
            quadrant:            Quadrant  = self.getQuadrant(quadrantCoordinates)
            while quadrant.hasStarBase is False:
                quadrantCoordinates = self._intelligence.generateQuadrantCoordinates()
                quadrant            = self.getQuadrant(quadrantCoordinates)

                self.logger.debug(f"StarBase at quadrant {quadrantCoordinates}")
                quadrant.addStarBase()
                starBaseCount -= 1

    def _setInitialQuadrant(self):
        """"""
        coordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
        self.logger.info(f'Current Quadrant set to: {coordinates}')

        row: QuadrantRow = self.quadrants[coordinates.y]
        self._currentQuadrant = row[coordinates.x]

    def __placeKlingonsInGalaxy(self):
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

    def __placeCommandersInGalaxy(self):
        """
        """
        for x in range(self._gameState.remainingCommanders):
            coordinates = self._intelligence.generateQuadrantCoordinates()
            quadrant    = self.getQuadrant(coordinates)
            quadrant.addCommander()

    def __placeSuperCommandersInGalaxy(self):
        """
        """
        for x in range(self._gameState.remainingSuperCommanders):
            coordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
            # if self._gameSettings.debugCollectSuperCommanderQuadrantCoordinates is True:
            #     self._debugSuperCommanderQuadrants.append(coordinates)
            quadrant    = self.getQuadrant(coordinates)
            quadrant.addSuperCommander()

    def _debugPrintKlingonPlacement(self):
        """
        """
        for y in range(GALAXY_ROWS):
            quadRow = self.quadrants[y]
            for x in range(GALAXY_COLUMNS):
                quadrant = quadRow[x]
                quadrant: Quadrant = cast(Quadrant, quadrant)
                self.logger.info(f'Quadrant({x},{y}) Klingon Count: {quadrant.klingonCount}')
