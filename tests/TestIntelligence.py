
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.GameType import GameType
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.PlayerType import PlayerType

from pytrek.model.Coordinates import Coordinates
from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase


class TestIntelligence(TestBase):

    DEFAULT_GAME_LENGTH: float         = 210.00

    EXPECTED_SHORT_GAME_LENGTH:  int = 56
    EXPECTED_LONG_GAME_LENGTH:   int = 224
    EXPECTED_MEDIUM_GAME_LENGTH: int = 112

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIntelligence.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        self.logger: Logger = TestIntelligence.clsLogger

        self.smarty:    Intelligence = Intelligence()
        self._settings: GameSettings = GameSettings()

        self._savePlayerType: PlayerType = self._settings.playerType
        self._saveGameType:   GameType   = self._settings.gameType

    def tearDown(self):

        self._settings.playerType = self._savePlayerType
        self._settings.gameType   = self._saveGameType

    def testGetRandomSectorCoordinates(self):
        """"""
        coordinates: Coordinates = self.smarty.generateSectorCoordinates()
        self.assertIsNotNone(coordinates, "Should not be null")
        self.logger.info("random coordinates: '%s'", coordinates)

        bogusCoordinate = Coordinates(-1, -1)

        self.assertNotEqual(coordinates, bogusCoordinate, "Not truly initializing random coordinates")

    def testInitialKlingonCountPlayerTypeNoviceGameTypeShort(self):
        """"""

        settings: GameSettings = self._settings
        settings.skill         = PlayerType.Novice
        settings.gameType      = GameType.Short

        intelligence = self.smarty

        klingonCount = intelligence.generateInitialKlingonCount(remainingGameTime=TestIntelligence.DEFAULT_GAME_LENGTH)

        self.assertIsNotNone(klingonCount, "I need some value back")

    def testInitialKlingonCountPlayerTypeEmeritusGameTypeLong(self):
        """"""

        settings          = self._settings
        settings.skill    = PlayerType.Emeritus
        settings.gameType = GameType.Long

        intelligence = Intelligence()
        klingonCount = intelligence.generateInitialKlingonCount(remainingGameTime=TestIntelligence.DEFAULT_GAME_LENGTH)
        self.assertIsNotNone(klingonCount, "I need some klingon value back")

    def testGetGameInitialTimeShort(self):
        """"""
        settings: GameSettings = self._settings

        settings.gameType = GameType.Short

        gameTime = self.smarty.generateInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(TestIntelligence.EXPECTED_SHORT_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialGameTimeLong(self):
        """"""
        settings: GameSettings = self._settings

        settings.gameType = GameType.Long

        gameTime = self.smarty.generateInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(TestIntelligence.EXPECTED_LONG_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialGameTimeMedium(self):
        """"""
        settings: GameSettings = self._settings

        settings.gameType = GameType.Medium

        gameTime = self.smarty.generateInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(TestIntelligence.EXPECTED_MEDIUM_GAME_LENGTH, gameTime, "Looks like game length factor changed")


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutVisibilityEnum))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
