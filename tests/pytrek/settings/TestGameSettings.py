
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds

from tests.TestBase import TestBase


class TestGameSettings(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

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

    def testDefaultWarpFactorExistence(self):
        self.assertIsNotNone(self._settings.defaultWarpFactor)

    def testPhaserFactor(self):
        self.assertEqual(2.0, self._settings.phaserFactor, 'Looks like we change the default phaser power factor')

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

    def testMinCommanderFiringIntervalExistence(self):
        self.assertIsNotNone(self._settings.minCommanderFiringInterval)

    def testMaxCommanderFiringIntervalExistence(self):
        self.assertIsNotNone(self._settings.maxCommanderFiringInterval)

    def testPhaserBurstToTerminateExistence(self):
        self.assertIsNotNone(self._settings.phaserBurstToTerminate)

    def testNoviceTorpedoSpeeds(self):

        tpNovice: TorpedoSpeeds = self._settings.noviceTorpedoSpeeds

        self.assertIsNotNone(tpNovice, 'We should at least get an object back')

        self.assertEqual(-1, tpNovice.superCommander)

    def testFairTorpedoSpeeds(self):

        tpFair: TorpedoSpeeds = self._settings.fairTorpedoSpeeds

        self.assertIsNotNone(tpFair, 'We should at least get an object back')

        self.assertEqual(-1, tpFair.superCommander)

    def testGoodTorpedoSpeeds(self):

        tpGood: TorpedoSpeeds = self._settings.goodTorpedoSpeeds

        self.assertIsNotNone(tpGood, 'We should at least get an object back')

        self.assertEqual(4, tpGood.superCommander)

    def testExpertTorpedoSpeeds(self):

        tpExpert: TorpedoSpeeds = self._settings.expertTorpedoSpeeds

        self.assertIsNotNone(tpExpert, 'We should at least get an object back')

        self.assertEqual(4, tpExpert.commander)
        self.assertEqual(4, tpExpert.superCommander)

    def testEmeritusTorpedoSpeeds(self):

        tpEmeritus: TorpedoSpeeds = self._settings.emeritusTorpedoSpeeds

        self.assertIsNotNone(tpEmeritus, 'We should at least get an object back')

        self.assertEqual(5, tpEmeritus.commander)
        self.assertEqual(5, tpEmeritus.superCommander)

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
