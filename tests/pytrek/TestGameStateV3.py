
from os import environ as osEnvironment

from pathlib import Path

from subprocess import run as subProcessRun

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase
from codeallybasic.ConfigurationLocator import XDG_CONFIG_HOME_ENV_VAR

from pytrek.Constants import APPLICATION_NAME

from pytrek.GameStateV3 import GameStateV3
from pytrek.GameStateV3 import JSON_FILENAME
from pytrek.engine.GameType import GameType
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
        # Create a fake XDG Path, so we do not overwrite any standard Game State
        fakeXDGPATH:   Path = Path('/tmp/fakeXDG/.config')
        self._appPath: Path = fakeXDGPATH / APPLICATION_NAME

        testGameState: str  = UnitTestBase.getFullyQualifiedResourceFileName(fileName=JSON_FILENAME, package=ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME)

        self._fqFileNamePath: Path = Path(testGameState)
        destFile:       Path = self._appPath / APPLICATION_NAME
        if destFile.exists() is True:
            destFile.unlink(missing_ok=True)
            self._appPath.rmdir()

        self._appPath.mkdir(parents=True, exist_ok=True)

        osEnvironment[XDG_CONFIG_HOME_ENV_VAR] = fakeXDGPATH.as_posix()

        command: str = f'cp {self._fqFileNamePath} {self._appPath}'

        subProcessRun([command], shell=True, capture_output=True, text=True, check=False)

    def tearDown(self):
        super().tearDown()

    def testSingleBehavior(self):

        gm1: GameStateV3 = GameStateV3()
        gm2: GameStateV3 = GameStateV3()
        self.assertEqual(gm1, gm2, 'Singleton behavior not enforced')

        gm1Id: str = f'{hex(id(gm1))}'
        gm2Id: str = f'{hex(id(gm2))}'

        self.assertEqual(gm1Id, gm2Id, 'Not the same')
        self.logger.warning(f'{gm1Id=} {gm2Id=}')

    def testRestore(self):

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
        # These we will save
        gameState.energy   = 9999.0
        gameState.starDate = 42.0
        gameState.gameType = GameType.Long
        gameState.currentQuadrantCoordinates = Coordinates(9, 9)

        gameState.save()
        # Change them other values
        gameState.energy   = 0.1
        gameState.starDate = 0.2
        gameState.gameType = GameType.Short
        gameState.currentQuadrantCoordinates = Coordinates(6, 6)

        gameState.restore()
        self.assertEqual(9999.0, gameState.energy, 'Did not restore saved data')
        self.assertEqual(42.0, gameState.starDate, 'Did not restore saved data')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestGameStateV3))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
