
from os import environ as osEnvironment

from pathlib import Path

from subprocess import run as subProcessRun
from subprocess import CompletedProcess

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pytrek.ConfigurationLocator import XDG_CONFIG_HOME_ENV_VAR

from pytrek.GameStateV3 import GameStateV3
from pytrek.GameStateV3 import JSON_FILENAME
from pytrek.engine.PlayerType import PlayerType
from pytrek.model.Coordinates import Coordinates

from pytrek.settings.SettingsCommon import SettingsCommon

from tests.ProjectTestBase import ProjectTestBase


class TestGameStateV3(ProjectTestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        SettingsCommon.determineSettingsLocation()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testRestore(self):

        fakeXDGPATH:    Path = Path('/tmp/fakeXDG/.config')
        appPath:        Path = fakeXDGPATH / 'pytrek'
        fqFileName:     str = UnitTestBase.getFullyQualifiedResourceFileName(fileName=JSON_FILENAME, package=ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME)
        fqFileNamePath: Path = Path(fqFileName)
        destFile:       Path = appPath / 'pytrek'
        if destFile.exists() is True:
            destFile.unlink(missing_ok=True)
            appPath.rmdir()

        appPath.mkdir(parents=True, exist_ok=True)

        osEnvironment[XDG_CONFIG_HOME_ENV_VAR] = fakeXDGPATH.as_posix()

        command: str = (
            f'cp {fqFileNamePath} {appPath}'
        )
        completedProcess: CompletedProcess = subProcessRun([command], shell=True, capture_output=True, text=True, check=False)

        self.assertTrue(completedProcess.returncode == 0, 'Setup did not work')

        gameState: GameStateV3 = GameStateV3()

        gameState = gameState.restore()
        #
        # Look at stuff we know is in the test game state
        #
        self.assertEqual(66666.0, gameState.starDate, 'Test star date has changed')
        self.assertEqual(PlayerType.Emeritus, gameState.playerType, 'Test game type has changed')
        self.assertEqual(Coordinates(7, 7), gameState.currentSectorCoordinates, 'Sector coordinates are bogus')
        self.assertEqual(True, gameState.gameActive, 'The game active state is wrong')

        self.logger.info(f'{gameState.starDate=}')

    def testSave(self):
        # Save defaults
        gameState: GameStateV3 = GameStateV3()

        gameState.save()

        # self.assertEqual(9999.0, gameState.energy, 'Did not restore saved data')
        # self.assertEqual(42.0, gameState.starDate, 'Did not restore saved data')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestGameStateV3))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
