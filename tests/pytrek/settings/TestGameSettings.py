
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.GameSettings import GameSettings

from tests.TestBase import TestBase


class TestGameSettings(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGameSettings.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger:    Logger       = TestGameSettings.clsLogger
        self._settings: GameSettings = GameSettings()

    def tearDown(self):
        pass

    def testMaxStarsExistence(self):
        self.assertIsNotNone(self._settings.maximumStars)

    def testMaxStarBasesExistence(self):
        self.assertIsNotNone(self._settings.maximumStarBases)

    def testMinStarBasesExistence(self):
        self.assertIsNotNone(self._settings.minimumStarBases)

    def testMaxPlanetsExistence(self):
        self.assertIsNotNone(self._settings.maximumPlanets)

    def testInitialEnergyLevelExistence(self):
        self.assertIsNotNone(self._settings.initialEnergyLevel)

    def testInitialShieldEnergyExistence(self):
        self.assertIsNotNone(self._settings.initialShieldEnergy)

    def testInitialTorpedoCountExistence(self):
        self.assertIsNotNone(self._settings.initialTorpedoCount)

    def testMinimumImpulseEnergyExistence(self):
        self.assertIsNotNone(self._settings.minimumImpulseEnergy)

    def testPlayerTypeExistence(self):
        self.assertIsNotNone(self._settings.playerType)

    def testGameTypeExistence(self):
        self.assertIsNotNone(self._settings.gameType)

    def testGameLengthFactorExistence(self):
        self.assertIsNotNone(self._settings.gameLengthFactor)

    def testStarBaseExtenderExistence(self):
        self.assertIsNotNone(self._settings.starBaseExtender)

    def testStarBaseMultiplierExistence(self):
        self.assertIsNotNone(self._settings.starBaseMultiplier)

    def testMinKlingonFiringIntervalExistence(self):
        self.assertIsNotNone(self._settings.minKlingonFiringInterval)

    def testMaxKlingonFiringIntervalExistence(self):
        self.assertIsNotNone(self._settings.maxKlingonFiringInterval)

    def testDebugSettingsAddKlingons(self):

        saveSetting: bool = self._settings.debugAddKlingons
        self._settings.debugAddKlingons = True
        self.assertTrue(self._settings.debugAddKlingons, 'Supposed to change')
        self._settings.debugAddKlingons = saveSetting

    def testDebugSettingsDebugKlingonCount(self):

        saveSetting: int = self._settings.debugKlingonCount
        self._settings.debugKlingonCount = 22
        self.assertEqual(22, self._settings.debugKlingonCount, 'Supposed to change')
        self._settings.debugKlingonCount = saveSetting

    def testDebugPrintKlingonPlacement(self):

        saveSetting: bool = self._settings.debugPrintKlingonPlacement
        self._settings.debugPrintKlingonPlacement = True
        self.assertTrue(self._settings.debugPrintKlingonPlacement, 'Should have changed to non-default')
        self._settings.debugPrintKlingonPlacement = saveSetting


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameSettings))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
