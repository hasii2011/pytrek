from pathlib import Path
from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.ShipCondition import ShipCondition
from pytrek.engine.GameType import GameType
from pytrek.engine.PlayerType import PlayerType

from pytrek.model.Coordinates import Coordinates

from tests.ProjectTestBase import ProjectTestBase

from pytrek.GameState import GameState

import json


TEST_GAME_STATE: str = """
{
    "energy": 7777,
    "shieldEnergy": 6666,
    "inTime": 512.0,
    "opTime": 0.0,
    "starDate": 20797,
    "remainingGameTime": 512.0,
    "remainingKlingons": 78,
    "remainingCommanders": 15,
    "remainingSuperCommanders": 8,
    "torpedoCount": 8888,
    "shipCondition": "Docked",
    "playerType": "Emeritus",
    "gameType": "Short",
    "currentQuadrantCoordinates": {
        "x": 6,
        "y": 6
    },
    "currentSectorCoordinates": {
        "x": 7,
        "y": 7
    },
    "starBaseCount": 4,
    "planetCount": 10
}
"""


class TestGameState(ProjectTestBase):

    # TEST_PICKLE_FILENAME: str = 'GameStats.json'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        gState: GameState = GameState()

        fqFileName: Path = gState.gameStateFileName

        if Path.exists(fqFileName) is True:
            fqFileName.rename(f'{fqFileName}.SAVE')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        gState: GameState = GameState()

        fqFileName: Path = gState.gameStateFileName

        fqFileName.unlink(missing_ok=True)

        saveFile: Path = Path(f'{fqFileName}.SAVE')

        if Path.exists(saveFile) is True:
            saveFile.rename(fqFileName)

    def setUp(self):
        super().setUp()
        self.resetSingletons()

    def tearDown(self):
        super().tearDown()

    def testSerialization(self):

        gState: GameState = GameState()
        gState.playerType = PlayerType.Emeritus
        gState.gameType   = GameType.Medium
        gState.starDate   = 40501.0

        gState.remainingGameTime = 42.42424242

        gState.currentQuadrantCoordinates = Coordinates(4, 4)
        gState.currentSectorCoordinates   = Coordinates(9, 9)

        gameStateJson = json.dumps(gState.toJson(), indent=4)

        self.logger.info(f'{gameStateJson}')

        self.logger.info("Decode JSON formatted Data")
        gStateDict = json.loads(gameStateJson)
        self.logger.info(f'{gStateDict}')

        self.logger.info(f'{ShipCondition("Green")=}')
        self.logger.info(f'{PlayerType.toEnum("Emeritus")=}')
        self.logger.info(f'{GameType.toEnum("Medium")=}')

    def testRestoreState(self):

        # get startup state
        gState: GameState = GameState()
        gState.currentQuadrantCoordinates = Coordinates(4, 4)
        gState.currentSectorCoordinates   = Coordinates(9, 9)

        saveKlingonCount: int = gState.remainingKlingons

        gState.saveState()

        self.resetSingletons()
        # Get a new one
        newGState: GameState = GameState()
        newGState.restoreState()

        self.assertEqual(saveKlingonCount, newGState.remainingKlingons, 'Not restored correctly')

    def testDeSerialize(self):

        gState: GameState = GameState()

        gStateDict = json.loads(TEST_GAME_STATE)

        self.logger.info(f'{gStateDict}')

        gState.fromDictionary(gStateDict)

        self.assertEqual(7777, gState.energy,       'Energy not restored')
        self.assertEqual(8888, gState.torpedoCount, 'Torpedo count not accurate')
        self.assertEqual(ShipCondition.Docked, gState.shipCondition, 'Ship condition enumeration not correct')
        self.assertEqual(GameType.Short,       gState.gameType,      'Game type enumeration not correct')

        self.assertEqual(Coordinates(x=6, y=6), gState.currentQuadrantCoordinates, 'Quadrant coordinates not correct')
        self.assertEqual(Coordinates(x=7, y=7), gState.currentSectorCoordinates,   'Sector coordinates not correct')

    def testSaveState(self):

        gState: GameState = GameState()
        gState.currentQuadrantCoordinates = Coordinates(7, 7)
        gState.currentSectorCoordinates   = Coordinates(7, 7)

        gState.saveState()


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestGameState))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
