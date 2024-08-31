
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceManager import DeviceManager

from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType
from pytrek.gui.MessageConsoleProxy import MessageConsoleProxy
from pytrek.gui.MessageConsoleSection import MessageConsoleSection

from pytrek.model.Galaxy import Galaxy

from pytrek.settings.GameSettings import GameSettings

from pytrek.GameState import GameState

from tests.ProjectTestBase import ProjectTestBase


class TestEventEngine(ProjectTestBase):
    """
    """
    clsGameSettings:      GameSettings      = cast(GameSettings, None)
    clsGameState:         GameState         = cast(GameState, None)
    clsGameEngine:        GameEngine        = cast(GameEngine, None)
    clsEventEngine:       EventEngine       = cast(EventEngine, None)
    clsDevices:           DeviceManager           = cast(DeviceManager, None)
    clsIntelligence:      Intelligence      = cast(Intelligence, None)
    clsGalaxy:            Galaxy            = cast(Galaxy, None)

    clsMessageConsoleProxy:   MessageConsoleProxy   = cast(MessageConsoleProxy, None)
    clsMessageConsoleSection: MessageConsoleSection = cast(MessageConsoleSection, None)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        TestEventEngine._setupGame()
        #
        # The game engine initializes the game state object (for better or worse)
        #
        self._gameSettings:      GameSettings      = TestEventEngine.clsGameSettings
        self._intelligence:      Intelligence      = TestEventEngine.clsIntelligence
        self._gameEngine:        GameEngine        = TestEventEngine.clsGameEngine
        self._gameState:         GameState         = TestEventEngine.clsGameState
        self._eventEngine:       EventEngine       = TestEventEngine.clsEventEngine
        self._devices:           DeviceManager     = TestEventEngine.clsDevices
        self._galaxy:            Galaxy            = TestEventEngine.clsGalaxy

        self._messageConsoleProxy:   MessageConsoleProxy   = TestEventEngine.clsMessageConsoleProxy
        self._messageConsoleSection: MessageConsoleSection = TestEventEngine.clsMessageConsoleSection

    def testEventUnSchedulable(self):

        # currentDate: float       = self._gameState.starDate
        fEvent:      FutureEvent = self._eventEngine.getEvent(FutureEventType.TRACTOR_BEAM)
        fireDate:    float       = fEvent.starDate
        #
        # Bump the game clock so this event fires
        #
        saveBaseCount:  int = self._gameState.starBaseCount
        saveCommanders: int = self._gameState.remainingCommanders

        self._gameState.starDate = fireDate + 1.0
        self._gameState.remainingCommanders = 0    # Ensure there are none
        self._gameState.starBaseCount       = 0

        self._eventEngine.makeUnSchedulable(FutureEventType.SUPER_NOVA)
        self._eventEngine.makeUnSchedulable(FutureEventType.COMMANDER_ATTACKS_BASE)

        self.logger.info(f'Updated star date: {self._gameState.starDate:.2f}')
        self._eventEngine._checkEvents(currentStarDate=self._gameState.starDate)

        fEvent = self._eventEngine.getEvent(FutureEventType.TRACTOR_BEAM)

        self.assertTrue(fEvent.schedulable is False, 'Game State should indicate we cannot do this')

        self._gameState.starBaseCount       = saveBaseCount
        self._gameState.remainingCommanders = saveCommanders

    def testCommanderAttacksBaseEventHandler(self):

        self._eventEngine.makeUnSchedulable(FutureEventType.SUPER_NOVA)
        self._eventEngine.makeUnSchedulable(FutureEventType.TRACTOR_BEAM)

        currentDate: float       = self._gameState.starDate
        fEvent:      FutureEvent = self._eventEngine.getEvent(FutureEventType.COMMANDER_ATTACKS_BASE)
        fireDate:    float       = fEvent.starDate
        #
        # Bump the game clock so this event fires
        #
        self._gameState.starDate = fireDate + 1.0

        self.logger.info(f'{self._gameState.remainingCommanders=}')

        self.logger.info(f'Star Date updated from {currentDate:.2f} to {self._gameState.starDate:.2f}')

        self._eventEngine._checkEvents(currentStarDate=self._gameState.starDate)

        fEvent = self._eventEngine.getEvent(FutureEventType.COMMANDER_ATTACKS_BASE)

        newFireDate: float = fEvent.starDate
        self.logger.info(f'newFireDate: {newFireDate:.2f}')

        if (newFireDate > fireDate) is False:
            self.logger.error(f'newFireDate: {newFireDate:.2f}   fireDate: {fireDate:.2f}')
            self.logger.error(f'{self._eventEngine=}')
        self.assertTrue(newFireDate > fireDate, 'It was supposed to be rescheduled')

    @classmethod
    def _setupGame(cls):
        """

        Since the game mechanics are run by singletons set them up once
        at the start of this test class.  Then each instance test will just
        use the pre-initialized singletons

        The initialization code copied from PyTrekView
        TODO: perhaps should go in a utility class so it is always current

        """
        ProjectTestBase.resetSingletons()

        TestEventEngine.clsGameSettings      = GameSettings()     # Be able to read the preferences file
        TestEventEngine.clsIntelligence      = Intelligence()

        TestEventEngine.clsGameState         = GameState()        # Set up the game parameters which uses the above
        TestEventEngine.clsGameState.currentQuadrantCoordinates = TestEventEngine.clsIntelligence.generateQuadrantCoordinates()

        TestEventEngine.clsGameEngine        = GameEngine()       # Then the engine needs to be initialized

        TestEventEngine.clsDevices           = DeviceManager()
        TestEventEngine.clsGalaxy            = Galaxy()

        TestEventEngine.clsMessageConsoleSection = MessageConsoleSection(left=0, bottom=0, width=100, height=100)
        TestEventEngine.clsMessageConsoleProxy   = MessageConsoleProxy()

        TestEventEngine.clsMessageConsoleProxy.console = TestEventEngine.clsMessageConsoleSection

        TestEventEngine.clsEventEngine       = EventEngine(TestEventEngine.clsMessageConsoleProxy)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestEventEngine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
