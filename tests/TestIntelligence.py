
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.Constants import MAX_KLINGON_FIRING_INTERVAL
from pytrek.Constants import MIN_KLINGON_FIRING_INTERVAL
from pytrek.engine.GameType import GameType
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.PlayerType import PlayerType

from pytrek.model.Coordinates import Coordinates
from pytrek.model.DataTypes import LRScanCoordinatesList
from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase


class TestIntelligence(TestBase):

    DEFAULT_GAME_LENGTH: float         = 210.00

    EXPECTED_SHORT_GAME_LENGTH:  int = 56
    EXPECTED_LONG_GAME_LENGTH:   int = 224
    EXPECTED_MEDIUM_GAME_LENGTH: int = 112

    MAX_STAR_DATE_CALLS: int = 7
    MAX_COORDINATES_COUNT:        int = 8
    NORTH_EDGE_COORDINATES_COUNT: int = 5

    SOUTH_EDGE_COORDINATES_COUNT: int = NORTH_EDGE_COORDINATES_COUNT
    EAST_EDGE_COORDINATES_COUNT:  int = SOUTH_EDGE_COORDINATES_COUNT
    WEST_EDGE_COORDINATES_COUNT:  int = EAST_EDGE_COORDINATES_COUNT

    NORTH_WEST_EDGE_COORDINATES_COUNT: int = 3
    NORTH_EAST_EDGE_COORDINATES_COUNT: int = NORTH_WEST_EDGE_COORDINATES_COUNT
    SOUTH_EAST_EDGE_COORDINATES_COUNT: int = NORTH_EAST_EDGE_COORDINATES_COUNT
    SOUTH_WEST_EDGE_COORDINATES_COUNT: int = SOUTH_EAST_EDGE_COORDINATES_COUNT

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIntelligence.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        self.logger: Logger = TestIntelligence.clsLogger

        self.smarty:    Intelligence = Intelligence()
        self._settings: GameSettings = GameSettings()

        self._savePlayerType: PlayerType = self._settings.playerType
        self._saveGameType:   GameType   = self._settings.gameType

    def tearDown(self):

        self._settings.playerType = self._savePlayerType
        self._settings.gameType   = self._saveGameType

    def testGetRandomSectorCoordinates(self):
        """"""
        coordinates: Coordinates = self.smarty.generateSectorCoordinates()
        self.assertIsNotNone(coordinates, "Should not be null")
        self.logger.info("random coordinates: '%s'", coordinates)

        bogusCoordinate = Coordinates(-1, -1)

        self.assertNotEqual(coordinates, bogusCoordinate, "Not truly initializing random coordinates")

    def testInitialKlingonCountPlayerTypeNoviceGameTypeShort(self):
        """"""

        settings: GameSettings = self._settings
        settings.skill         = PlayerType.Novice
        settings.gameType      = GameType.Short

        intelligence = self.smarty

        klingonCount = intelligence.generateInitialKlingonCount(remainingGameTime=TestIntelligence.DEFAULT_GAME_LENGTH)

        self.assertIsNotNone(klingonCount, "I need some value back")

    def testInitialKlingonCountPlayerTypeEmeritusGameTypeLong(self):
        """"""

        settings          = self._settings
        settings.skill    = PlayerType.Emeritus
        settings.gameType = GameType.Long

        intelligence = Intelligence()
        klingonCount = intelligence.generateInitialKlingonCount(remainingGameTime=TestIntelligence.DEFAULT_GAME_LENGTH)
        self.assertIsNotNone(klingonCount, "I need some klingon value back")

    def testGetGameInitialTimeShort(self):
        """"""
        settings: GameSettings = self._settings

        settings.gameType = GameType.Short

        gameTime = self.smarty.generateInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(TestIntelligence.EXPECTED_SHORT_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialGameTimeLong(self):
        """"""
        settings: GameSettings = self._settings

        settings.gameType = GameType.Long

        gameTime = self.smarty.generateInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(TestIntelligence.EXPECTED_LONG_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialGameTimeMedium(self):
        """"""
        settings: GameSettings = self._settings

        settings.gameType = GameType.Medium

        gameTime = self.smarty.generateInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(TestIntelligence.EXPECTED_MEDIUM_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialStarDate(self):

        for x in range(0, TestIntelligence.MAX_STAR_DATE_CALLS):
            starDate: int = self.smarty.generateInitialStarDate()
            self.assertIsNotNone(starDate)
            self.assertGreater(starDate, 0, "No such thing as a 0 star date")
            self.logger.debug(f"Initial stardate '{starDate}'")

    def testGenerateAdjacentCoordinatesBase(self):
        """
        No need to test value of coordinates that is done by another unit test
        """
        baseCoordinates: Coordinates = Coordinates(x=4, y=4)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.MAX_COORDINATES_COUNT, len(coordinateList), "We should get all directional coordinates")

    def testGenerateAdjacentCoordinatesNorth(self):
        """
        Place center quadrant on northern edge
        """
        baseCoordinates: Coordinates = Coordinates(x=4, y=0)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.NORTH_EDGE_COORDINATES_COUNT, len(coordinateList), "We should get all directional coordinates")

    def testGenerateAdjacentCoordinatesSouth(self):
        """
        Place center quadrant on southern edge
        """
        baseCoordinates: Coordinates = Coordinates(x=4, y=9)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.SOUTH_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testGenerateAdjacentCoordinatesEast(self):
        """
        Place center quadrant on eastern edge
        """
        baseCoordinates: Coordinates = Coordinates(x=9, y=4)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.EAST_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testGenerateAdjacentCoordinatesWest(self):
        """
        Place center quadrant on western edge
        """
        baseCoordinates: Coordinates = Coordinates(x=0, y=4)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.WEST_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testGenerateAdjacentCoordinatesNorthWest(self):
        """
        Place center quadrant on north western edge
        """
        baseCoordinates: Coordinates = Coordinates(x=0, y=0)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.NORTH_WEST_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testGenerateAdjacentCoordinatesNorthEast(self):
        """
        Place center quadrant on north eastern edge
        """
        baseCoordinates: Coordinates = Coordinates(x=9, y=0)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.NORTH_EAST_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testGenerateAdjacentCoordinatesSouthEast(self):
        """
        Place center quadrant on south eastern edge
        """
        baseCoordinates: Coordinates = Coordinates(x=0, y=9)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.SOUTH_EAST_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testGenerateAdjacentCoordinatesSouthWest(self):
        """
        Place center quadrant on south western edge
        """
        baseCoordinates: Coordinates = Coordinates(x=0, y=9)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.SOUTH_WEST_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testRand(self):

        for x in range(0, 100):
            ans = self.smarty.rand()
            self.logger.debug(f"testRand - Iteration {x}, answer is {ans}")

    def testComputeKlingonFiringInterval(self):
        for x in range(0, 100):
            ans: int = self.smarty.computeKlingonFiringInterval()
            self.assertGreaterEqual(ans, MIN_KLINGON_FIRING_INTERVAL, 'Cannot be below the min')
            self.assertLessEqual(ans, MAX_KLINGON_FIRING_INTERVAL, 'Cannot be above the  max')
            self.logger.debug(f'Random klingon firing interval: {ans}')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIntelligence))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
