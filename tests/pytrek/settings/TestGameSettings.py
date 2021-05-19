
from logging import Logger
from logging import getLogger

from os import remove as osRemove
from os import path as osPath

from shutil import copyfile

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.Constants import BACKUP_SUFFIX

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

    def setUp(self):
        self.logger:    Logger = TestGameSettings.clsLogger
        self._settings: GameSettings = GameSettings()

    def tearDown(self):
        pass

    def testSettingExistence(self):
        """
        Only tests the existence of settings not their default value
        """
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

    def testMinKlingonFiringInterval(self):
        self.assertIsNotNone(self._settings.minKlingonFiringInterval)

    def testMaxKlingonFiringInterval(self):
        self.assertIsNotNone(self._settings.maxKlingonFiringInterval)

    def testDebugSettingsAddKlingons(self):

        self._backupSettings()
        self._emptySettings()
        self._settings.init()       # create defaults

        self._settings.debugAddKlingons = True

        self.assertTrue(self._settings.debugAddKlingons, 'Supposed to change')

        self._restoreBackup()

    def testDebugSettingsDebugKlingonCount(self):

        self._backupSettings()
        self._emptySettings()
        self._settings.init()       # create defaults

        self._settings.debugKlingonCount = 6

        self.assertEqual(6, self._settings.debugKlingonCount, 'Supposed to change')

        self._restoreBackup()

    def testDebugPrintKlingonPlacement(self):
        self._backupSettings()
        self._emptySettings()
        self._settings.init()       # create defaults

        self._settings.debugPrintKlingonPlacement = True

        self.assertTrue(self._settings.debugPrintKlingonPlacement, 'Should have changed to non-default')

        self._restoreBackup()

    def _backupSettings(self):

        settingsFileName: str = SettingsCommon.getSettingsLocation()

        source: str = settingsFileName
        target: str = f"{settingsFileName}{BACKUP_SUFFIX}"
        if osPath.exists(source):
            try:
                copyfile(source, target)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

    def _restoreBackup(self):

        settingsFileName: str = SettingsCommon.getSettingsLocation()

        source: str = f"{settingsFileName}{BACKUP_SUFFIX}"
        target: str = settingsFileName
        if osPath.exists(source):
            try:
                copyfile(source, target)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

            osRemove(source)
        else:
            osRemove(target)

    def _emptySettings(self):

        self._settings: GameSettings = GameSettings()
        self._settings._createEmptySettings()
        self._settings._settingsCommon.saveSettings()


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameSettings))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
