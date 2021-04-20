
from logging import Logger
from logging import getLogger
from typing import TextIO

import jsonpickle

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.GameType import GameType
from pytrek.engine.PlayerType import PlayerType

from pytrek.model.Coordinates import Coordinates

from tests.TestBase import TestBase

from pytrek.GameState import GameState


class TestGameState(TestBase):

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGameState.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestGameState.clsLogger

    def tearDown(self):
        pass

    def testJsonSerialization(self):

        gState: GameState = GameState()
        gState.skill      = PlayerType.Emeritus
        gState.gameType   = GameType.Medium
        gState.starDate   = 40501.0

        gState.remainingGameTime = 42.42424242

        gState.currentQuadrantCoordinates = Coordinates(4, 4)
        gState.currentSectorCoordinates   = Coordinates(9, 9)

        jsonGState: str = jsonpickle.encode(gState, indent=4)
        self.assertIsNotNone(jsonGState, "Pickling failed")

        self.logger.info("json game stats: '%s", jsonGState)

        file: TextIO = open('GameStats.json', 'w')
        file.write(jsonGState)
        file.close()

        jsonFile: TextIO = open("GameStats.json", 'r')
        jsonStr  = jsonFile.read()
        self.assertIsNotNone(jsonStr)
        jsonFile.close()

        thawedGameState: GameState = jsonpickle.decode(jsonStr)
        self.assertIsNotNone(thawedGameState, "Did that thaw")

        self.assertEqual(gState.skill,             thawedGameState.skill,             "Skill did not thaw")
        self.assertEqual(gState.gameType,          thawedGameState.gameType,          "Game type did not thaw")
        self.assertEqual(gState.starDate,          thawedGameState.starDate,          "Star date did not thaw")
        self.assertEqual(gState.remainingGameTime, thawedGameState.remainingGameTime, "Remaining game time did not thaw")


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGameState))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
