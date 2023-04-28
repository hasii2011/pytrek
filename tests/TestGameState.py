
from typing import TextIO

from os import remove as osRemove

import jsonpickle

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.GameType import GameType
from pytrek.engine.PlayerType import PlayerType

from pytrek.model.Coordinates import Coordinates

from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase

from pytrek.GameState import GameState


class TestGameState(TestBase):

    TEST_PICKLE_FILENAME: str = 'GameStats.json'

    @classmethod
    def setUpClass(cls):
        TestBase.setUpClass()
        SettingsCommon.determineSettingsLocation()

    def testJsonSerialization(self):

        pass
        gState: GameState = GameState()
        gState.playerType = PlayerType.Emeritus
        gState.gameType   = GameType.Medium
        gState.starDate   = 40501.0

        gState.remainingGameTime = 42.42424242

        gState.currentQuadrantCoordinates = Coordinates(4, 4)
        gState.currentSectorCoordinates   = Coordinates(9, 9)

        jsonGState: str = jsonpickle.encode(gState, indent=4)
        self.assertIsNotNone(jsonGState, "Pickling failed")

        self.logger.info(f'json game stats: {jsonGState}')

        file: TextIO = open(TestGameState.TEST_PICKLE_FILENAME, 'w')
        file.write(jsonGState)
        file.close()

        jsonFile: TextIO = open(TestGameState.TEST_PICKLE_FILENAME, 'r')
        jsonStr:  str    = jsonFile.read()
        self.assertIsNotNone(jsonStr)
        jsonFile.close()

        thawedGameState: GameState = jsonpickle.decode(jsonStr)
        self.assertIsNotNone(thawedGameState, "Did that thaw?")

        self.assertEqual(gState.playerType,        thawedGameState.playerType,        "Player type did not thaw")
        self.assertEqual(gState.gameType,          thawedGameState.gameType,          "Game type did not thaw")
        self.assertEqual(gState.starDate,          thawedGameState.starDate,          "Star date did not thaw")
        self.assertEqual(gState.remainingGameTime, thawedGameState.remainingGameTime, "Remaining game time did not thaw")

        osRemove(TestGameState.TEST_PICKLE_FILENAME)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameState))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
