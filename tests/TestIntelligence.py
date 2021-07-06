from statistics import mode
from typing import List

from logging import Logger
from logging import getLogger

from statistics import median
from statistics import mean


from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.GameState import GameState
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.GameType import GameType
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.PlayerType import PlayerType
from pytrek.gui.gamepieces.PlanetType import PlanetType

from pytrek.model.Coordinates import Coordinates
from pytrek.model.DataTypes import LRScanCoordinatesList
from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds

from tests.TestBase import TestBase


class TestIntelligence(TestBase):

    DEFAULT_GAME_LENGTH: float         = 210.00

    EXPECTED_SHORT_GAME_LENGTH:  int = 56
    EXPECTED_LONG_GAME_LENGTH:   int = 224
    EXPECTED_MEDIUM_GAME_LENGTH: int = 112

    MAX_STAR_DATE_CALLS:          int = 7
    MAX_COORDINATES_COUNT:        int = 8
    NORTH_EDGE_COORDINATES_COUNT: int = 5

    SOUTH_EDGE_COORDINATES_COUNT: int = NORTH_EDGE_COORDINATES_COUNT
    EAST_EDGE_COORDINATES_COUNT:  int = SOUTH_EDGE_COORDINATES_COUNT
    WEST_EDGE_COORDINATES_COUNT:  int = EAST_EDGE_COORDINATES_COUNT

    NORTH_WEST_EDGE_COORDINATES_COUNT: int = 3
    NORTH_EAST_EDGE_COORDINATES_COUNT: int = NORTH_WEST_EDGE_COORDINATES_COUNT
    SOUTH_EAST_EDGE_COORDINATES_COUNT: int = NORTH_EAST_EDGE_COORDINATES_COUNT
    SOUTH_WEST_EDGE_COORDINATES_COUNT: int = SOUTH_EAST_EDGE_COORDINATES_COUNT

    GENERATE_KLINGON_COUNT_LOOP_COUNT: int = 250
    COMMAND_POWER_LOOP_COUNT:          int = 250

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIntelligence.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        self.logger: Logger = TestIntelligence.clsLogger

        self._gameEngine: GameEngine   = GameEngine()     # TODO: when https://github.com/hasii2011/PyArcadeStarTrek/issues/9 is fixed don't needs this
        self.smarty:      Intelligence = Intelligence()
        self._settings:   GameSettings = GameSettings()
        self._gameState:  GameState    = GameState()

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

        gameState: GameState  = self._gameState
        gameState.playerType  = PlayerType.Novice
        gameState.gameType    = GameType.Short

        medianCount: float = self._runKlingonCountTest()

        ans: bool = (medianCount >= 10.0) and (medianCount < 20.0)

        self.assertTrue(ans, f'We are not in range: {medianCount=}')

    def testInitialKlingonCountPlayerTypeEmeritusGameTypeLong(self):

        gameState: GameState  = self._gameState
        gameState.playerType  = PlayerType.Emeritus
        gameState.gameType = GameType.Long

        medianCount: float = self._runKlingonCountTest()

        ans: bool = (medianCount > 1050.0) and (medianCount < 1300.0)

        self.assertTrue(ans, f'We are not in range: {medianCount=}')

    def testInitialKlingonCountPlayerTypeGoodGameTypeMedium(self):

        gameState: GameState  = self._gameState
        gameState.playerType  = PlayerType.Good
        gameState.gameType = GameType.Medium

        medianCount: float = self._runKlingonCountTest()

        ans: bool = (medianCount > 150.0) and (medianCount < 250.0)

        self.assertTrue(ans, f'We are not in range: {medianCount=}')

    def testGenerateInitialSuperCommanderCountPlayerTypeNovice(self):

        self._runSuperCommanderCountTest(playerType=PlayerType.Novice, klingonCount=101, expectedSuperCommanderCount=10, assertionMsg='Novice Formula Changed')

    def testGenerateInitialSuperCommanderCountPlayerTypeGood(self):

        self._runSuperCommanderCountTest(playerType=PlayerType.Good, klingonCount=101, expectedSuperCommanderCount=10, assertionMsg='Good Formula Changed')

    def testGenerateInitialSuperCommanderCountPlayerTypeExpert(self):

        self._runSuperCommanderCountTest(playerType=PlayerType.Expert, klingonCount=100, expectedSuperCommanderCount=20, assertionMsg='Expert Formula Changed')

    def testGenerateInitialSuperCommanderCountPlayerTypeEmeritus(self):

        self._runSuperCommanderCountTest(playerType=PlayerType.Emeritus, klingonCount=100, expectedSuperCommanderCount=33, assertionMsg='Emeritus Changed')

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
            self.logger.debug(f"Initial StarDate '{starDate}'")

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

    def testRandomFloat(self):

        for x in range(0, 99):
            answer: float = self.smarty.randomFloat()
            self.logger.debug(f'testRandomFloat - Iteration {x}, {answer=}')

            self.assertGreater(answer, 0.0, 'Follow the specification please')
            self.assertLess(answer, 1.0, 'Follow the specification please')

    def testComputePlanetsInGalaxy(self):
        maxPlanets: int = self._settings.maximumPlanets
        for x in range(0, 10):
            answer: int = self.smarty.computePlanetsInGalaxy()
            self.logger.debug(f'testComputePlanetsInGalaxy1 - Iteration {x}, {answer=}')
            self.assertLessEqual(answer, maxPlanets, 'We cannot have too many')

    def testComputeKlingonFiringInterval(self):

        minFiringInterval: int = self._settings.minKlingonFiringInterval
        maxFiringInterval: int = self._settings.maxKlingonFiringInterval

        for x in range(0, 100):
            ans: int = self.smarty.computeKlingonFiringInterval()
            self.assertGreaterEqual(ans, minFiringInterval, 'Cannot be below the min')
            self.assertLessEqual(ans, maxFiringInterval, 'Cannot be above the  max')
            self.logger.debug(f'Random klingon firing interval: {ans}')

    def testComputeCommanderFiringInterval(self):

        minFiringInterval: int = self._settings.minCommanderFiringInterval
        maxFiringInterval: int = self._settings.maxCommanderFiringInterval

        generatedFiringIntervals: List[int] = []

        for x in range(0, 100):
            ans: int = self.smarty.computeCommanderFiringInterval()
            generatedFiringIntervals.append(ans)
            self.assertGreaterEqual(ans, minFiringInterval, 'Cannot be below the min')
            self.assertLessEqual(ans, maxFiringInterval, 'Cannot be above the  max')

        medianCount: int = median(generatedFiringIntervals)
        meanCount:   int = mean(generatedFiringIntervals)
        modeCount:   int = mode(generatedFiringIntervals)

        minValue: int = min(generatedFiringIntervals)
        maxValue: int = max(generatedFiringIntervals)
        statsStr: str = (
            f'median={medianCount} average={meanCount} mode={modeCount} {minValue=} {maxValue=}'
        )
        self.logger.info(statsStr)

        expectedMinValue: int = self._settings.minCommanderFiringInterval
        expectedMaxValue: int = self._settings.maxCommanderFiringInterval

        self.assertEqual(expectedMinValue, minValue, 'We are below the expected value')
        self.assertEqual(expectedMaxValue, maxValue, 'We are above the expected value')

    def testComputeSuperCommanderMoveInterval(self):

        minMoveInterval: int = self._settings.minSuperCommanderMoveInterval
        maxMoveInterval: int = self._settings.maxSuperCommanderMoveInterval

        generatedMoveIntervals: List[int] = []

        for x in range(0, 150):
            ans: int = self.smarty.computeSuperCommanderMoveInterval()
            generatedMoveIntervals.append(ans)
            self.assertGreaterEqual(ans, minMoveInterval, 'Cannot be below the min')
            self.assertLessEqual(ans, maxMoveInterval, 'Cannot be above the  max')

        medianCount: int = median(generatedMoveIntervals)
        meanCount:   int = mean(generatedMoveIntervals)
        modeCount:   int = mode(generatedMoveIntervals)

        minValue: int = min(generatedMoveIntervals)
        maxValue: int = max(generatedMoveIntervals)
        statsStr: str = (
            f'median={medianCount} average={meanCount} mode={modeCount} {minValue=} {maxValue=}'
        )
        self.logger.info(statsStr)

        expectedMinValue: int = self._settings.minSuperCommanderMoveInterval
        expectedMaxValue: int = self._settings.maxSuperCommanderMoveInterval

        self.assertEqual(expectedMinValue, minValue, 'We are below the expected value')
        self.assertEqual(expectedMaxValue, maxValue, 'We are above the expected value')

    def testComputeRandomPlanetType(self):
        for x in range(0, 10):
            planetType: PlanetType = self.smarty.computeRandomPlanetType()
            self.logger.debug(f'Random Choice: {planetType}')

    def testComputeCommanderPowerNovicePlayer(self):

        self._gameState.playerType  = PlayerType.Novice

        medianStatistic: float = self._runCommanderPowerTest()

        ans: bool = (medianStatistic > 1150.0) and (medianStatistic < 1240.0)

        self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeCommanderPowerEmeritusPlayer(self):

        self._gameState.playerType  = PlayerType.Emeritus

        medianStatistic: float = self._runCommanderPowerTest()

        ans: bool = (medianStatistic > 1360.0) and (medianStatistic < 1430.0)

        self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeCommanderPowerGoodPlayer(self):

        self._gameState.playerType  = PlayerType.Good

        medianStatistic: float = self._runCommanderPowerTest()

        ans: bool = (medianStatistic > 1265.0) and (medianStatistic < 1327.0)

        self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeCommanderMoveInterval(self):

        generatedMoveIntervals: List[int] = []
        for x in range(250):
            moveInterval: int = self.smarty.computeCommanderMoveInterval()
            generatedMoveIntervals.append(moveInterval)

        medianCount: int = median(generatedMoveIntervals)
        meanCount:   int = mean(generatedMoveIntervals)
        modeCount:   int = mode(generatedMoveIntervals)

        minValue: int = min(generatedMoveIntervals)
        maxValue: int = max(generatedMoveIntervals)
        statsStr: str = (
            f'median={medianCount} average={meanCount} mode={modeCount} {minValue=} {maxValue=}'
        )
        self.logger.info(statsStr)

        expectedMinValue: int = self._settings.minCommanderMoveInterval
        expectedMaxValue: int = self._settings.maxCommanderMoveInterval

        self.assertEqual(expectedMinValue, minValue, 'We are below the expected value')
        self.assertEqual(expectedMaxValue, maxValue, 'We are above the expected value')

    def testComputeKlingonMoveInterval(self):

        generatedMoveIntervals: List[int] = []

        for x in range(250):
            moveInterval: int = self.smarty.computeKlingonMoveInterval()
            generatedMoveIntervals.append(moveInterval)

        medianCount: int = median(generatedMoveIntervals)
        meanCount:   int = mean(generatedMoveIntervals)
        modeCount:   int = mode(generatedMoveIntervals)

        minValue: int = min(generatedMoveIntervals)
        maxValue: int = max(generatedMoveIntervals)
        statsStr: str = (
            f'median={medianCount} average={meanCount} mode={modeCount} {minValue=} {maxValue=}'
        )
        self.logger.info(statsStr)

        expectedMinValue: int = self._settings.minKlingonMoveInterval
        expectedMaxValue: int = self._settings.maxKlingonMoveInterval

        self.assertEqual(expectedMinValue, minValue, 'We are below the expected value')
        self.assertEqual(expectedMaxValue, maxValue, 'We are above the expected value')

    def testGetEmeritusTorpedoSpeeds(self):

        savePlayerType: PlayerType = self._gameState.playerType

        self._gameState.playerType = PlayerType.Emeritus

        tp: TorpedoSpeeds = self.smarty.getTorpedoSpeeds()

        self.assertEqual(PlayerType.Emeritus, tp.playerType, 'Looks like we got the wrong settings')
        self._gameState.playerType = savePlayerType

    def _runKlingonCountTest(self) -> float:

        gameState:    GameState    = self._gameState
        intelligence: Intelligence = self.smarty

        generatedCount: List[int] = []
        for x in range(TestIntelligence.GENERATE_KLINGON_COUNT_LOOP_COUNT):

            klingonCount = intelligence.generateInitialKlingonCount()
            generatedCount.append(klingonCount)

        medianCount: float = median(generatedCount)
        meanCount:   float = mean(generatedCount)
        modeCount:   float = mode(generatedCount)

        statsStr: str = (
            f' {gameState.playerType} {gameState.gameType} '
            f'median={medianCount} average={meanCount} mode={modeCount}'
        )
        self.logger.info(statsStr)

        return medianCount

    def _runCommanderPowerTest(self):

        intelligence: Intelligence = self.smarty

        generatedPower: List[float] = []

        for x in range(TestIntelligence.COMMAND_POWER_LOOP_COUNT):

            commanderPower: float = intelligence.computeCommanderPower()
            generatedPower.append(commanderPower)

        medianStatistic: float = median(generatedPower)
        meanStatistic:   float = mean(generatedPower)
        modeStatistic:   float = mode(generatedPower)

        statsStr: str = (
            f' {self._gameState.playerType} '
            f'median={medianStatistic:.2f} average={meanStatistic:.2f} mode={modeStatistic:.2f}'
        )
        self.logger.info(statsStr)

        return medianStatistic

    def _runSuperCommanderCountTest(self, playerType: PlayerType, klingonCount: int, expectedSuperCommanderCount: int, assertionMsg: str):

        self._gameState.playerType = playerType

        actualSuperCommanderCount: int = self.smarty.generateInitialSuperCommanderCount(numberOfKlingons=klingonCount)

        self.assertEqual(expectedSuperCommanderCount, actualSuperCommanderCount, assertionMsg)


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIntelligence))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
