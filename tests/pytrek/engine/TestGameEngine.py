
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.GameState import GameState
from pytrek.engine.PlayerType import PlayerType
from pytrek.engine.ShieldHitData import ShieldHitData
from pytrek.model.Coordinates import Coordinates
from pytrek.settings.SettingsCommon import SettingsCommon
from tests.TestBase import TestBase

from pytrek.engine.GameEngine import GameEngine


class TestGameEngine(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGameEngine.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        self.logger:      Logger     = TestGameEngine.clsLogger
        self._gameEngine: GameEngine = GameEngine()
        self._gameState:  GameState  = GameState()

    def tearDown(self):
        pass

    def testComputeShieldHit(self):

        for pType in PlayerType:
            torpedoHit:     float         = self._commonComputeHit(playerType=pType)
            shieldHitData:  ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=torpedoHit)
            self.logger.info(f"torpedoHit: f{torpedoHit:.2f}  {pType:19.19}  {shieldHitData}")

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

    def _commonComputeHit(self, playerType: PlayerType) -> float:

        self._gameState.skill = playerType

        shooterPosition: Coordinates = Coordinates(x=7, y=7)
        targetPosition:  Coordinates = Coordinates(x=3, y=7)
        klingonPower:    float       = 348.0

        computedHit = self._gameEngine.computeHit(shooterPosition=shooterPosition,
                                                  targetPosition=targetPosition,
                                                  klingonPower=klingonPower)

        return computedHit


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameEngine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
