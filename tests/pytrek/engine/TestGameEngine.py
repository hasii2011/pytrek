
from typing import Dict
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.Computer import Computer
from pytrek.engine.Direction import Direction
from pytrek.engine.DirectionData import DirectionData
from pytrek.engine.PlayerType import PlayerType
from pytrek.engine.ShieldHitData import ShieldHitData

from pytrek.model.Coordinates import Coordinates

from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase

from pytrek.engine.GameEngine import GameEngine

from pytrek.GameState import GameState


TestedDirections = NewType('TestedDirections', Dict[Direction, bool])


class TestGameEngine(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGameEngine.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        self.logger:      Logger     = TestGameEngine.clsLogger
        self._gameEngine: GameEngine = GameEngine()
        self._gameState:  GameState  = GameState()
        self._computer:   Computer   = Computer()

    def tearDown(self):
        pass

    def testDoPhasersMaxDistance(self):

        shooterCoordinates: Coordinates = Coordinates(0, 0)
        targetCoordinates:  Coordinates = Coordinates(9, 9)

        expectedPhaserHit: float = 218.6
        self._runPhaserTest(shooterCoordinates=shooterCoordinates, targetCoordinates=targetCoordinates, expectedPhaserHit=expectedPhaserHit)

    def testDoPhasersShortDistance(self):
        shooterCoordinates: Coordinates = Coordinates(0, 4)
        targetCoordinates:  Coordinates = Coordinates(4, 4)

        expectedPhaserHit: float = 239.68
        self._runPhaserTest(shooterCoordinates=shooterCoordinates, targetCoordinates=targetCoordinates, expectedPhaserHit=expectedPhaserHit)

    def testHitThem(self):
        shooterCoordinates: Coordinates = Coordinates(0, 0)
        targetCoordinates:  Coordinates = Coordinates(9, 9)
        distance:           float        = self._computer.computeQuadrantDistance(startSector=shooterCoordinates, endSector=targetCoordinates)
        enemyPower:         float        = 500.0

        powerDrain: float = self._gameEngine.hitThem(distance=distance, hit=218.6, enemyPower=enemyPower)

        minPowerDrain: float = 329

        self.assertGreater(powerDrain, minPowerDrain, 'Did not calculate the minimum power drain')

        self.logger.info(f'{powerDrain=}')

    def testComputeShieldHit(self):

        for pType in PlayerType:
            torpedoHit:     float         = self._commonComputeHit(playerType=pType)
            shieldHitData:  ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=torpedoHit)
            self.logger.info(f"torpedoHit: {torpedoHit:.2f}  {pType:19.19}  {shieldHitData}")

    def testComputeHit(self):

        for pType in PlayerType:

            computedHit = self._commonComputeHit(playerType=pType)
            self.assertFalse(computedHit == 0.0, "Can't have non-hit")
            self.logger.info(f"computedHit for {pType.__repr__()}: {computedHit}")

    def testComputeEnergyWhenBlockedNominal(self):

        startSector: Coordinates = Coordinates(x=1, y=1)
        endSector:   Coordinates = Coordinates(x=5, y=5)

        expectedStopEnergy: float = 76.57
        decimalPlace:       int   = 2

        stopEnergy: float = self._gameEngine.computeEnergyWhenBlocked(startSector=startSector, endSector=endSector)

        self.logger.info(f'{stopEnergy}')

        self.assertAlmostEqual(expectedStopEnergy, stopEnergy, decimalPlace, 'Nominal test does not compute')

    def testComputeEnergyWhenBlockedMaximum(self):

        startSector: Coordinates = Coordinates(x=1, y=1)
        endSector:   Coordinates = Coordinates(x=8, y=8)

        expectedStopEnergy: float = 118.99
        decimalPlace:       int   = 2

        stopEnergy: float = self._gameEngine.computeEnergyWhenBlocked(startSector=startSector, endSector=endSector)

        self.logger.info(f'{stopEnergy}')

        self.assertAlmostEqual(expectedStopEnergy, stopEnergy, decimalPlace, 'Maximum case does not compute')

    def testComputeEnergyWhenBlockedMinimum(self):

        startSector: Coordinates = Coordinates(x=1, y=1)
        endSector:   Coordinates = Coordinates(x=1, y=2)

        expectedStopEnergy: float = 30.0
        decimalPlace:       int   = 2

        stopEnergy: float = self._gameEngine.computeEnergyWhenBlocked(startSector=startSector, endSector=endSector)

        self.logger.info(f'{stopEnergy}')

        self.assertAlmostEqual(expectedStopEnergy, stopEnergy, decimalPlace, 'Minimum test does not compute')

    def testComputeCloseCoordinates(self):
        """
        Loop until all directions tested
        """
        testedDirections:  TestedDirections = self._initDirectionTest()
        targetCoordinates: Coordinates      = Coordinates(x=5, y=5)

        while self._areAllDirectionsValidated(testedDirections=testedDirections) is False:

            directionData:     DirectionData = self._gameEngine.computeCloseCoordinates(targetCoordinates=targetCoordinates)

            testedDirections[directionData.direction] = True
            self._validateReturn(targetCoordinates=targetCoordinates, directionData=directionData)

        self.logger.debug(f'All directions tested: {testedDirections=}')

    def _commonComputeHit(self, playerType: PlayerType) -> float:

        self._gameState.playerType = playerType

        shooterPosition: Coordinates = Coordinates(x=7, y=7)
        targetPosition:  Coordinates = Coordinates(x=3, y=7)
        klingonPower:    float       = 348.0

        computedHit = self._gameEngine.computeHit(shooterPosition=shooterPosition,
                                                  targetPosition=targetPosition,
                                                  klingonPower=klingonPower)

        return computedHit

    def _initDirectionTest(self) -> TestedDirections:

        testedDirections: TestedDirections = TestedDirections({})

        for direction in Direction:
            testedDirections[direction] = False

        return testedDirections

    def _validateReturn(self, targetCoordinates: Coordinates, directionData: DirectionData):

        direction:   Direction = directionData.direction
        coordinates: Coordinates = directionData.coordinates
        targetX: int = targetCoordinates.x
        targetY: int = targetCoordinates.y
        newX:    int = coordinates.x
        newY:    int = coordinates.y

        if direction == Direction.North:
            self.assertEqual(newX, targetX, 'X should be unchanged for North')
            self.assertEqual(newY, targetY - 1, 'Y should be less one for North')
        elif direction == Direction.South:
            self.assertEqual(newX, targetX, 'X should be unchanged for South')
            self.assertEqual(newY, targetY + 1, 'Y should be one more for South')
        elif direction == Direction.East:
            self.assertEqual(newX, targetX + 1, 'X should be one more for East')
            self.assertEqual(newY, targetY, 'Y should be unchanged for East')
        elif direction == Direction.West:
            self.assertEqual(newX, targetX - 1, 'X should be one less for West')
            self.assertEqual(newY, targetY, 'Y should be unchanged for West')
        elif direction == Direction.NorthEast:
            self.assertEqual(newX, targetX + 1, 'X should be one 1 more for NorthEast')
            self.assertEqual(newY, targetY - 1, 'Y should be 1 less for NorthEast')
        elif direction == Direction.SouthEast:
            self.assertEqual(newX, targetX + 1, 'X should be one 1 more for SouthEast')
            self.assertEqual(newY, targetY + 1, 'Y should be 1 more for SouthEast')
        elif direction == Direction.NorthWest:
            self.assertEqual(newX, targetX - 1, 'X should be one 1 less for NorthWest')
            self.assertEqual(newY, targetY - 1, 'Y should be 1 less for NorthWest')
        elif direction == Direction.SouthWest:
            self.assertEqual(newX, targetX - 1, 'X should be one 1 less for SouthWest')
            self.assertEqual(newY, targetY + 1, 'Y should be 1 more for SouthWest')

        self.logger.info(f'{direction.name} passed')

    def _areAllDirectionsValidated(self, testedDirections:  TestedDirections) -> bool:
        """

        Args:
            testedDirections: The tested directions dictionary

        Returns: False if at least one entry is True
        """
        for value in testedDirections.values():
            if value is False:
                return False
        return True

    def _runPhaserTest(self, shooterCoordinates: Coordinates, targetCoordinates: Coordinates, expectedPhaserHit: float):

        distance:           float        = self._computer.computeQuadrantDistance(startSector=shooterCoordinates, endSector=targetCoordinates)
        enemyPower:         float       = 500.0
        powerAmount:        float       = 500.0

        phaserHit: float = self._gameEngine.doPhasers(distance=distance, enemyPower=enemyPower, powerAmount=powerAmount)

        self.assertAlmostEqual(expectedPhaserHit, phaserHit, places=1)
        self.logger.info(f'{phaserHit=}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameEngine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
