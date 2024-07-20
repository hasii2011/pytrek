
from typing import cast
from typing import Callable
from typing import List

from itertools import count

from statistics import median
from statistics import mean
from statistics import mode

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.GameState import GameState
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.GameType import GameType
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.Intelligence import TractorBeamComputation
from pytrek.engine.PlayerType import PlayerType
from pytrek.gui.gamepieces.PlanetType import PlanetType

from pytrek.model.Coordinates import Coordinates
from pytrek.model.DataTypes import LRScanCoordinatesList
from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds

from tests.ProjectTestBase import ProjectTestBase

ComputeCallBack = Callable[[PlayerType], float]


class TestIntelligence(ProjectTestBase):

    DEFAULT_GAME_LENGTH: float  = 210.00
    DEFAULT_AVERAGE:     float  = 7.0

    EXPECTED_SHORT_GAME_LENGTH:  int = 512
    EXPECTED_LONG_GAME_LENGTH:   int = 2048
    EXPECTED_MEDIUM_GAME_LENGTH: int = 1024

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
    POWER_LOOP_COUNT:                  int = 250
    RANGE_TESTS_LOOP_COUNT:            int = 50
    MAX_STAR_BASE_CALLS:               int = 100
    EXPONENTIAL_RANDOM_MAX_CALLS:      int = 150
    BASE_ATTACK_INTERVAL_MAX_CALLS:    int = 150
    BASE_DESTROYED_INTERVAL_MAX_CALLS: int = 150

    @classmethod
    def setUpClass(cls):
        ProjectTestBase.setUpClass()
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        super().setUp()

        self._gameEngine:   GameEngine   = GameEngine()
        self._gameSettings: GameSettings = GameSettings()
        self._gameState:    GameState    = GameState()
        self.smarty:        Intelligence = Intelligence()

        self._savePlayerType: PlayerType = self._gameSettings.playerType
        self._saveGameType:   GameType   = self._gameSettings.gameType

        self._powerTestPlayerType: PlayerType = cast(PlayerType, None)

    def tearDown(self):
        super().tearDown()
        self._gameSettings.playerType = self._savePlayerType
        self._gameSettings.gameType   = self._saveGameType

    def testGetRandomSectorCoordinates(self):
        """"""
        coordinates: Coordinates = self.smarty.generateSectorCoordinates()
        self.assertIsNotNone(coordinates, "Should not be null")
        self.logger.info("random coordinates: '%s'", coordinates)

        bogusCoordinate = Coordinates(-1, -1)

        self.assertNotEqual(coordinates, bogusCoordinate, "Not truly initializing random coordinates")

    def testInitialKlingonCountPlayerTypeNoviceGameTypeShort(self):

        medianCount: float = self._runKlingonCountTest(gameType=GameType.Short, playerType=PlayerType.Novice)

        ans: bool = (medianCount >= 9.0) and (medianCount < 20.0)

        self.assertTrue(ans, f'We are not in range: {medianCount=}')

    def testInitialKlingonCountPlayerTypeEmeritusGameTypeLong(self):

        medianCount: float = self._runKlingonCountTest(gameType=GameType.Long, playerType=PlayerType.Emeritus)

        ans: bool = (medianCount > 1050.0) and (medianCount < 1300.0)

        self.assertTrue(ans, f'We are not in range: {medianCount=}')

    def testInitialKlingonCountPlayerTypeGoodGameTypeMedium(self):

        medianCount: float = self._runKlingonCountTest(gameType=GameType.Medium, playerType=PlayerType.Good)

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
        settings: GameSettings = self._gameSettings

        settings.gameType = GameType.Short

        gameTime = self.smarty.generateInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(TestIntelligence.EXPECTED_SHORT_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialGameTimeLong(self):
        """"""
        settings: GameSettings = self._gameSettings

        settings.gameType = GameType.Long

        gameTime = self.smarty.generateInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(TestIntelligence.EXPECTED_LONG_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialGameTimeMedium(self):
        """"""
        settings: GameSettings = self._gameSettings

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
        Place center quadrant on northwestern edge
        """
        baseCoordinates: Coordinates = Coordinates(x=0, y=0)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.NORTH_WEST_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testGenerateAdjacentCoordinatesNorthEast(self):
        """
        Place center quadrant on northeastern edge
        """
        baseCoordinates: Coordinates = Coordinates(x=9, y=0)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.NORTH_EAST_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testGenerateAdjacentCoordinatesSouthEast(self):
        """
        Place center quadrant on southeastern edge
        """
        baseCoordinates: Coordinates = Coordinates(x=0, y=9)

        coordinateList: LRScanCoordinatesList = self.smarty.generateAdjacentCoordinates(centerCoordinates=baseCoordinates)

        self.assertIsNotNone(coordinateList)
        self.assertEqual(TestIntelligence.SOUTH_EAST_EDGE_COORDINATES_COUNT, len(coordinateList), "We should not get all directional coordinates")

    def testGenerateAdjacentCoordinatesSouthWest(self):
        """
        Place center quadrant on southwestern edge
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
        maxPlanets: int = self._gameSettings.maximumPlanets
        for x in range(0, 10):
            answer: int = self.smarty.generateInitialPlanetCount()
            self.logger.debug(f'testComputePlanetsInGalaxy1 - Iteration {x}, {answer=}')
            self.assertLessEqual(answer, maxPlanets, 'We cannot have too many')

    def testComputeKlingonFiringInterval(self):

        minFiringInterval: int = self._gameSettings.minKlingonFiringInterval
        maxFiringInterval: int = self._gameSettings.maxKlingonFiringInterval

        for x in range(0, 100):
            ans: int = self.smarty.computeKlingonFiringInterval()
            self.assertGreaterEqual(ans, minFiringInterval, 'Cannot be below the min')
            self.assertLessEqual(ans, maxFiringInterval, 'Cannot be above the  max')
            self.logger.debug(f'Random klingon firing interval: {ans}')

    def testComputeCommanderFiringInterval(self):

        minFiringInterval: int = self._gameSettings.minCommanderFiringInterval
        maxFiringInterval: int = self._gameSettings.maxCommanderFiringInterval

        generatedFiringIntervals: List[int] = []

        for x in range(0, 100):
            ans: int = self.smarty.computeCommanderFiringInterval()
            generatedFiringIntervals.append(ans)
            self.assertGreaterEqual(ans, minFiringInterval, 'Cannot be below the min')
            self.assertLessEqual(ans, maxFiringInterval, 'Cannot be above the  max')

        medianCount: int = self._toInt(median(generatedFiringIntervals))
        meanCount:   int = self._toInt(mean(generatedFiringIntervals))
        modeCount:   int = mode(generatedFiringIntervals)

        minValue: int = min(generatedFiringIntervals)
        maxValue: int = max(generatedFiringIntervals)
        statsStr: str = (
            f'median={medianCount} average={meanCount} mode={modeCount} {minValue=} {maxValue=}'
        )
        self.logger.info(statsStr)

        expectedMinValue: int = self._gameSettings.minCommanderFiringInterval
        expectedMaxValue: int = self._gameSettings.maxCommanderFiringInterval

        self.assertEqual(expectedMinValue, minValue, 'We are below the expected value')
        self.assertEqual(expectedMaxValue, maxValue, 'We are above the expected value')

    def testComputeSuperCommanderMoveInterval(self):

        minMoveInterval: int = self._gameSettings.minSuperCommanderMoveInterval
        maxMoveInterval: int = self._gameSettings.maxSuperCommanderMoveInterval

        generatedMoveIntervals: List[int] = []

        for x in range(0, 150):
            ans: int = self.smarty.computeSuperCommanderMoveInterval()
            generatedMoveIntervals.append(ans)
            self.assertGreaterEqual(ans, minMoveInterval, 'Cannot be below the min')
            self.assertLessEqual(ans, maxMoveInterval, 'Cannot be above the  max')

        medianCount: int = self._toInt(median(generatedMoveIntervals))
        meanCount:   int = self._toInt(mean(generatedMoveIntervals))
        modeCount:   int = mode(generatedMoveIntervals)

        minValue: int = min(generatedMoveIntervals)
        maxValue: int = max(generatedMoveIntervals)
        statsStr: str = (
            f'median={medianCount} average={meanCount} mode={modeCount} {minValue=} {maxValue=}'
        )
        self.logger.info(statsStr)

        expectedMinValue: int = self._gameSettings.minSuperCommanderMoveInterval
        expectedMaxValue: int = self._gameSettings.maxSuperCommanderMoveInterval

        self.assertEqual(expectedMinValue, minValue, 'We are below the expected value')
        self.assertEqual(expectedMaxValue, maxValue, 'We are above the expected value')

    def testComputeRandomPlanetType(self):
        for x in range(0, 10):
            planetType: PlanetType = self.smarty.computeRandomPlanetType()
            self.logger.debug(f'Random Choice: {planetType}')

    def testComputeCommanderPowerNovicePlayer(self):

        self._powerTestPlayerType = PlayerType.Novice
        for x in range(TestIntelligence.RANGE_TESTS_LOOP_COUNT):
            medianStatistic: float = self._runPowerTest(computeCallback=self.smarty.computeCommanderPower)
            ans:              bool = (medianStatistic > 1150.0) and (medianStatistic < 1252.0)

            self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeCommanderPowerEmeritusPlayer(self):

        self._powerTestPlayerType = PlayerType.Emeritus

        for x in range(TestIntelligence.RANGE_TESTS_LOOP_COUNT):
            medianStatistic: float = self._runPowerTest(computeCallback=self.smarty.computeCommanderPower)
            ans:             bool  = (medianStatistic >= 1348.0) and (medianStatistic <= 1452.0)

            self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeCommanderPowerGoodPlayer(self):

        self._powerTestPlayerType = PlayerType.Good

        for x in range(TestIntelligence.RANGE_TESTS_LOOP_COUNT):
            medianStatistic: float = self._runPowerTest(computeCallback=self.smarty.computeCommanderPower)
            ans:             bool = (medianStatistic >= 1248.0) and (medianStatistic <= 1349.0)

            self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeSuperCommanderPowerEmeritusPlayer(self):

        self._powerTestPlayerType = PlayerType.Emeritus

        for x in range(TestIntelligence.RANGE_TESTS_LOOP_COUNT):
            medianStatistic: float = self._runPowerTest(computeCallback=self.smarty.computeCommanderPower)
            ans:             bool = (medianStatistic > 1289.0) and (medianStatistic < 1452.0)
            self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeSuperCommanderPowerExpertPlayer(self):

        self._powerTestPlayerType = PlayerType.Expert

        for x in range(TestIntelligence.RANGE_TESTS_LOOP_COUNT):
            medianStatistic: float = self._runPowerTest(computeCallback=self.smarty.computeCommanderPower)
            ans:              bool = (medianStatistic >= 1300.0) and (medianStatistic <= 1402.0)
            self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeCommanderMoveInterval(self):

        generatedMoveIntervals: List[int] = []
        for x in range(250):
            moveInterval: int = self.smarty.computeCommanderMoveInterval()
            generatedMoveIntervals.append(moveInterval)

        medianCount: int = self._toInt(median(generatedMoveIntervals))
        meanCount:   int = self._toInt(mean(generatedMoveIntervals))
        modeCount:   int = mode(generatedMoveIntervals)

        minValue: int = min(generatedMoveIntervals)
        maxValue: int = max(generatedMoveIntervals)
        statsStr: str = (
            f'median={medianCount} average={meanCount} mode={modeCount} {minValue=} {maxValue=}'
        )
        self.logger.info(statsStr)

        expectedMinValue: int = self._gameSettings.minCommanderMoveInterval
        expectedMaxValue: int = self._gameSettings.maxCommanderMoveInterval

        self.assertEqual(expectedMinValue, minValue, 'We are below the expected value')
        self.assertEqual(expectedMaxValue, maxValue, 'We are above the expected value')

    def testComputeKlingonMoveInterval(self):

        generatedMoveIntervals: List[int] = []

        for x in range(250):
            moveInterval: int = self.smarty.computeKlingonMoveInterval()
            generatedMoveIntervals.append(moveInterval)

        medianCount: int = self._toInt(median(generatedMoveIntervals))
        meanCount:   int = self._toInt(mean(generatedMoveIntervals))
        modeCount:   int = mode(generatedMoveIntervals)

        minValue: int = min(generatedMoveIntervals)
        maxValue: int = max(generatedMoveIntervals)
        statsStr: str = (
            f'median={medianCount} average={meanCount} mode={modeCount} {minValue=} {maxValue=}'
        )
        self.logger.info(statsStr)

        expectedMinValue: int = self._gameSettings.minKlingonMoveInterval
        expectedMaxValue: int = self._gameSettings.maxKlingonMoveInterval

        self.assertEqual(expectedMinValue, minValue, 'We are below the expected value')
        self.assertEqual(expectedMaxValue, maxValue, 'We are above the expected value')

    def testGetEmeritusTorpedoSpeeds(self):

        tp: TorpedoSpeeds = self.smarty.getTorpedoSpeeds(playerType=PlayerType.Emeritus)

        self.assertEqual(PlayerType.Emeritus, tp.playerType, 'Looks like we got the wrong settings')

    def testGenerateInitialStarBaseCount(self):

        minimumStarBases: int = self._gameSettings.minimumStarBases
        maximumStarBases: int = self._gameSettings.maximumStarBases

        generatedCount: List[int] = []
        for x in range(0, TestIntelligence.MAX_STAR_BASE_CALLS):
            starBaseCount: int = self.smarty.generateInitialStarBaseCount()

            self.assertLessEqual(starBaseCount, maximumStarBases,    'Too many StarBases generated')
            self.assertGreaterEqual(starBaseCount, minimumStarBases, 'Too few StarBases generated')
            generatedCount.append(starBaseCount)

        medianStatistic: float = median(generatedCount)
        meanStatistic:   float = mean(generatedCount)
        modeStatistic:   float = mode(generatedCount)

        statsStr: str = (
            f'Initial StarBase count statistics: '
            f'median={medianStatistic:.2f} average={meanStatistic:.2f} mode={modeStatistic:.2f}'
        )
        self.logger.info(statsStr)

    def testExponentialRandom(self):

        self.logger.info(f"DEFAULT: {TestIntelligence.DEFAULT_AVERAGE}")

        for x in range(0, TestIntelligence.EXPONENTIAL_RANDOM_MAX_CALLS):
            ans: float = self.smarty.exponentialRandom(TestIntelligence.DEFAULT_AVERAGE)
            self.assertGreater(11924.00, ans, 'Average failed upper bound')

    def testExponentialRandomFiftySix(self):
        for x in range(0, TestIntelligence.EXPONENTIAL_RANDOM_MAX_CALLS):
            ans2: float = self.smarty.exponentialRandom(56.0)
            self.assertGreater(902.00, ans2, '56 failed upper bound')

    def testExponentialRandomLongerGameTime(self):

        self._gameSettings.gameType = GameType.Long
        initGameTime: float = self.smarty.generateInitialGameTime()

        for x in range(0, TestIntelligence.EXPONENTIAL_RANDOM_MAX_CALLS):
            ans: float = self.smarty.exponentialRandom(initGameTime)
            self.assertGreater(21286.00, ans, 'Longer Game Time failed upper bound')

    def testComputeBaseAttackInterval(self):

        intervals: List[float] = []
        for x in count():
            if x > TestIntelligence.BASE_ATTACK_INTERVAL_MAX_CALLS:
                break
            initialGameTime: float = self.smarty.generateInitialGameTime()
            interval:        float = self.smarty.computeBaseAttackInterval(inTime=initialGameTime)
            intervals.append(interval)

        medianStatistic: float = median(intervals)
        meanStatistic:   float = mean(intervals)
        modeStatistic:   float = mode(intervals)

        statsStr: str = (
            f'Base Attack Interval: '
            f'median={medianStatistic:.2f} average={meanStatistic:.2f} mode={modeStatistic:.2f}'
        )
        self.logger.info(statsStr)

        ans: bool = (medianStatistic > 21.0) and (medianStatistic < 526.0)
        self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeBaseDestroyedInterval(self):
        intervals: List[float] = []
        for x in count():
            if x > TestIntelligence.BASE_DESTROYED_INTERVAL_MAX_CALLS:
                break
            interval:        float = self.smarty.computeBaseDestroyedInterval()
            intervals.append(interval)

        medianStatistic: float = median(intervals)
        meanStatistic:   float = mean(intervals)
        modeStatistic:   float = mode(intervals)

        statsStr: str = (
            f'BaseDestroyedInterval: '
            f'median={medianStatistic:.2f} average={meanStatistic:.2f} mode={modeStatistic:.2f}'
        )
        self.logger.info(statsStr)

        ans: bool = (medianStatistic > 2.0) and (medianStatistic < 4.0)
        self.assertTrue(ans, f'We are not in range: {medianStatistic=}')

    def testComputeTractorBeamFactors(self):

        expendedEnergy: float = 200.00

        factors: TractorBeamComputation = self.smarty.computeTractorBeamFactors(energy=expendedEnergy)

        self.assertTrue(6.0 <= factors.warpFactor <= 8.0, msg='The answer is not close enough')

    def _runKlingonCountTest(self, gameType: GameType, playerType: PlayerType) -> float:

        gameState:    GameState    = self._gameState
        intelligence: Intelligence = self.smarty

        generatedCount: List[int] = []
        for x in range(TestIntelligence.GENERATE_KLINGON_COUNT_LOOP_COUNT):

            klingonCount = intelligence.generateInitialKlingonCount(gameType=gameType, playerType=playerType)
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

    def _runPowerTest(self, computeCallback: ComputeCallBack):

        generatedPower: List[float] = []

        for x in range(TestIntelligence.POWER_LOOP_COUNT):

            commanderPower: float = computeCallback(self._powerTestPlayerType)

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

        actualSuperCommanderCount: int = self.smarty.generateInitialSuperCommanderCount(playerType=playerType, numberOfKlingons=klingonCount)

        self.assertEqual(expectedSuperCommanderCount, actualSuperCommanderCount, assertionMsg)

    def _toInt(self, floatValue: float) -> int:
        return round(floatValue)


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIntelligence))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
