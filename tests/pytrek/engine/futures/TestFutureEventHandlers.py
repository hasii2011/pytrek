
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.GameState import GameState

from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase

from pytrek.engine.futures.FutureEventHandlers import FutureEventHandlers


class TestFutureEventHandlers(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    clsGameSettings: GameSettings = cast(GameSettings, None)
    clsGameState:    GameState    = cast(GameState, None)
    clsGameEngine:   GameEngine   = cast(GameEngine, None)
    clsIntelligence: Intelligence = cast(Intelligence, None)
    clsComputer:     Computer     = cast(Computer, None)
    clsGalaxy:       Galaxy       = cast(Galaxy, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestFutureEventHandlers.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()
        TestFutureEventHandlers._setupGame()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestFutureEventHandlers.clsLogger

        self._gameSettings: GameSettings = TestFutureEventHandlers.clsGameSettings
        self._gameState:    GameState    = TestFutureEventHandlers.clsGameState
        self._gameEngine:   GameEngine   = TestFutureEventHandlers.clsGameEngine
        self._intelligence: Intelligence = TestFutureEventHandlers.clsIntelligence
        self._computer:     Computer     = TestFutureEventHandlers.clsComputer
        self._galaxy:       Galaxy       = TestFutureEventHandlers.clsGalaxy

        self._eventHandlers: FutureEventHandlers = FutureEventHandlers()

    def tearDown(self):
        pass

    def testSuperNovaEventHandlerKlingonsAreDead(self):

        quadrant: Quadrant = self._getANovaEventQuadrant()

        beforeSuperNovaKlingonsCount: int = self._gameState.remainingKlingons
        quadrantKlingons:             int = quadrant.klingonCount

        self._eventHandlers.superNovaEventHandler(quadrant=quadrant)

        self.assertEqual(0, quadrant.klingonCount, 'Not all klingons are dead')

        expectedRemainingKlingons: int = beforeSuperNovaKlingonsCount - quadrantKlingons
        actualKlingonCount:        int = self._gameState.remainingKlingons
        self.assertEqual(expectedRemainingKlingons, actualKlingonCount, 'Game State was not updated for klingons')

    def testSuperNovaEventHandlerCommandersAreDead(self):

        quadrant: Quadrant = self._getANovaEventQuadrant()

        beforeSuperNovaCommandersCount: int = self._gameState.remainingCommanders
        quadrantCommanders:             int = quadrant.klingonCount

        self._eventHandlers.superNovaEventHandler(quadrant=quadrant)

        self.assertEqual(0, quadrant.klingonCount, 'Not all klingons are dead')

        expectedRemainingCommanders: int = beforeSuperNovaCommandersCount - quadrantCommanders
        actualCommanderCount:        int = self._gameState.remainingCommanders
        self.assertEqual(expectedRemainingCommanders, actualCommanderCount, 'Game State was not updated for commanders')

    def testTractorBeamEventHandler(self):
        """Another test"""
        pass

    def testCommanderAttacksBaseEventHandler(self):
        """Another test"""
        pass

    def _getANovaEventQuadrant(self) -> Quadrant:

        coordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
        quadrant: Quadrant = Quadrant(coordinates=coordinates)
        quadrant.addKlingon()
        quadrant.addCommander()
        quadrant.addSuperCommander()
        quadrant.addStarBase()
        #
        # Update the game state to reflect what I did here
        #
        self._gameState.remainingKlingons        += 1
        self._gameState.remainingCommanders      += 1
        self._gameState.remainingSuperCommanders += 1
        # self._gameState.remainingStarBase += 1    # TODO we need to maintain this statistic

        return quadrant

    @classmethod
    def _setupGame(cls):
        """
        Assumes the game setting location has been set

        Since the game mechanics are run by singletons set them up once
        at the start of this test class.  Then each instance test will just
        use the pre-initialized singletons

        The initializaton code copied from PyTrekView
        TODO: perhaps should go in a utility class so it is always current

        """
        # These singletons are initialized for the first time
        TestFutureEventHandlers.clsGameSettings = GameSettings()     # Be able to read the preferences file
        TestFutureEventHandlers.clsGameState    = GameState()        # Set up the game parameters which uses the above
        TestFutureEventHandlers.clsGameEngine   = GameEngine()       # Then the engine needs to be initialized
        TestFutureEventHandlers.clsIntelligence = Intelligence()
        TestFutureEventHandlers.clsComputer     = Computer()
        TestFutureEventHandlers.clsGalaxy       = Galaxy()           # This essentially finishes initializing most of the game


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestFutureEventHandlers))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
