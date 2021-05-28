
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
        TestGameSettings.backupSettings()

    @classmethod
    def tearDownClass(cls):
        TestGameSettings.restoreBackup()

    def setUp(self):
        self.logger:    Logger = TestGameSettings.clsLogger

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

        self._settings.debugAddKlingons = True

        self.assertTrue(self._settings.debugAddKlingons, 'Supposed to change')

    def testDebugSettingsDebugKlingonCount(self):

        self._settings.debugKlingonCount = 22

        self.assertEqual(22, self._settings.debugKlingonCount, 'Supposed to change')

    def testDebugPrintKlingonPlacement(self):

        self._settings.debugPrintKlingonPlacement = True

        self.assertTrue(self._settings.debugPrintKlingonPlacement, 'Should have changed to non-default')

    @classmethod
    def backupSettings(cls):

        settingsFileName: str = SettingsCommon.getSettingsLocation()

        source: str = settingsFileName
        target: str = f"{settingsFileName}{BACKUP_SUFFIX}"
        print(f'Backup to: {target}')
        if osPath.exists(source):
            try:
                copyfile(source, target)
            except IOError as e:
                TestGameSettings.clsLogger.error(f"Unable to copy file. {e}")

    @classmethod
    def restoreBackup(cls):

        settingsFileName: str = SettingsCommon.getSettingsLocation()

        source: str = f"{settingsFileName}{BACKUP_SUFFIX}"
        target: str = settingsFileName

        # self.__printBackupFile(source)

        print(f'Restoring: {source}')
        if osPath.exists(source):
            try:
                copyfile(source, target)
            except IOError as e:
                TestGameSettings.clsLogger.error(f"Unable to copy file. {e}")

            # osRemove(source)
        else:
            osRemove(target)

    def __printBackupFile(self, filename: str):

        f = open(filename, "r")
        contents: str = f.read()
        print(f'***************************')
        print(f'{filename=}')
        print(contents)
        print(f'***************************')

        f.close()


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameSettings))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
