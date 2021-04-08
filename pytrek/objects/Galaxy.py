
from typing import NewType
from typing import cast
from typing import List

import logging

# from org.hasii.pytrek.Settings import Settings
from pytrek import Constants
from pytrek.Singleton import Singleton
from pytrek.engine.Intelligence import Intelligence
from pytrek.objects.Coordinates import Coordinates
from pytrek.objects.Quadrant import Quadrant

# from org.hasii.pytrek.GameStatistics import GameStatistics

QuadrantRow = NewType('QuadrantRow', List[Quadrant])
GalaxyGrid  = NewType('GalaxyGrid', List[QuadrantRow])


class Galaxy(Singleton):
    """
    Galaxy management
    """

    def init(self, screen, intelligence, gameEngine):
        """"""
        self.screen         = screen
        self.intelligence   = intelligence
        self.gameEngine     = gameEngine

        # self.stats          = GameStatistics()
        # self.settings       = Settings()
        self.logger         = logging.getLogger(__name__)

        self.starBaseCount: int = 0
        self.planetCount:   int = 0
        # self.gameParameters:  GameStatistics = cast(GameStatistics, None)
        self.currentQuadrant: Quadrant   = cast(Quadrant, None)
        self.quadrants:       GalaxyGrid = GalaxyGrid([])  # 2D array aka python list

        self.createGalaxy()

        # self.placeKlingonsInGalaxy()
        # self.placeCommandersInGalaxy()
        # self.placeStarBasesInGalaxy()
        # self.setInitialQuadrant()

    def createGalaxy(self):

        self.quadrants = []
        for y in range(Constants.GALAXY_ROWS):
            quadrantRow: QuadrantRow = QuadrantRow([])
            for x in range(Constants.GALAXY_COLUMNS):
                coordinates = Coordinates(x, y)
                quadrant = Quadrant(coordinates)
                quadrantRow.append(quadrant)
                self.logger.warning(f"Created quadrant: ({x},{y})")
            self.quadrants.append(quadrantRow)

    def updateGalaxy(self):
        """"""

    def setInitialQuadrant(self):
        """"""
        coordinates = self.intelligence.getRandomQuadrantCoordinates()
        self.logger.info("Current Quadrant set to: %s", coordinates)
        row = self.quadrants[coordinates.getX()]
        self.currentQuadrant = row[coordinates.getY()]

    def getCurrentQuadrant(self) -> Quadrant:
        """"""
        return self.currentQuadrant

    def placeKlingonsInGalaxy(self):
        """"""
        for x in range(self.stats.remainingKlingons):
            coordinates = self.intelligence.getRandomQuadrantCoordinates()
            quadrant    = self.getQuadrant(coordinates)
            quadrant.addKlingon()
        self.debugPrintKlingonPlacement()

    def placeCommandersInGalaxy(self):
        """"""
        for x in range(self.stats.remainingCommanders):
            coordinates = self.intelligence.getRandomQuadrantCoordinates()
            quadrant    = self.getQuadrant(coordinates)
            quadrant.addCommander()

    def placeStarBasesInGalaxy(self):
        """"""
        starBaseCount = self.intelligence.getInitialStarBaseCount()
        while starBaseCount != 0:
            quadrantCoordinates = self.intelligence.getRandomQuadrantCoordinates()
            quadrant            = self.getQuadrant(quadrantCoordinates)
            while quadrant.hasStarBase() is True:
                quadrantCoordinates = self.intelligence.getRandomQuadrantCoordinates()
                quadrant = self.getQuadrant(quadrantCoordinates)

            self.logger.debug(f"Starbase at quadrant {quadrantCoordinates}")
            quadrant.addStarBase()
            starBaseCount -= 1

    def getQuadrant(self, quadrantCoordinates: Coordinates) -> Quadrant:

        quadrantRow: QuadrantRow = self.quadrants[quadrantCoordinates.y]
        quadrant:    Quadrant    = quadrantRow[quadrantCoordinates.y]

        return quadrant

    def debugPrintKlingonPlacement(self):
        """"""
        for x in range(Intelligence.GALAXY_HEIGHT):
            quadRow = self.quadrants[x]
            for y in range(Intelligence.GALAXY_WIDTH):
                quadrant = quadRow[y]
                self.logger.debug("Quadrant(%s,%s) Klingon Count %s", x, y, str(quadrant.getKlingonCount()))
