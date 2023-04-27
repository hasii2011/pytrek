

from logging import Logger
from logging import getLogger
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices

from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.model.Galaxy import Galaxy

from pytrek.settings.GameSettings import GameSettings

from pytrek.settings.SettingsCommon import SettingsCommon

from pytrek.GameState import GameState

from tests.TestBase import TestBase
from tests.LogMessageConsole import LogMessageConsole

BASIC_DAMAGE = 4.0


class TestEventEngine(TestBase):
    """
    """
    clsGameSettings:      GameSettings      = cast(GameSettings, None)
    clsGameState:         GameState         = cast(GameState, None)
    clsGameEngine:        GameEngine        = cast(GameEngine, None)
    clsLogMessageConsole: LogMessageConsole = cast(LogMessageConsole, None)
    clsEventEngine:       EventEngine       = cast(EventEngine, None)
    clsDevices:           Devices           = cast(Devices, None)
    clsIntelligence:      Intelligence      = cast(Intelligence, None)
    clsGalaxy:            Galaxy            = cast(Galaxy, None)

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()
        SettingsCommon.determineSettingsLocation()

        TestEventEngine._setupGame()

    def setUp(self):
        """"""
        self.logger:      Logger      = getLogger(__name__)
        #
        # The game engine initializes the game state object (for better or worse)
        #
        self._logMessageConsole: LogMessageConsole = TestEventEngine.clsLogMessageConsole
        self._gameSettings:      GameSettings      = TestEventEngine.clsGameSettings
        self._intelligence:      Intelligence      = TestEventEngine.clsIntelligence
        self._gameEngine:        GameEngine        = TestEventEngine.clsGameEngine
        self._gameState:         GameState         = TestEventEngine.clsGameState
        self._eventEngine:       EventEngine       = TestEventEngine.clsEventEngine
        self._devices:           Devices           = TestEventEngine.clsDevices
        self._galaxy:            Galaxy            = TestEventEngine.clsGalaxy

    def testEventUnSchedulable(self):

        self._setupGame()
        # currentDate: float       = self._gameState.starDate
        fEvent:      FutureEvent = self._eventEngine.getEvent(FutureEventType.TRACTOR_BEAM)
        fireDate:    float       = fEvent.starDate
        #
        # Bump the game clock so this event fires
        #
        self._gameState.starDate = fireDate + 1.0
        self._gameState.remainingCommanders = 0    # Ensure there are none
        self._gameState.starBaseCount       = 0

        self._eventEngine.makeUnSchedulable(FutureEventType.SUPER_NOVA)
        self._eventEngine.makeUnSchedulable(FutureEventType.COMMANDER_ATTACKS_BASE)

        self.logger.info(f'Updated star date: {self._gameState.starDate:.2f}')
        self._eventEngine._checkEvents(currentStarDate=self._gameState.starDate)

        fEvent = self._eventEngine.getEvent(FutureEventType.TRACTOR_BEAM)

        self.assertTrue(fEvent.schedulable is False, 'Game State should indicate we cannot do this')

    def testCommanderAttacksBaseEventHandler(self):

        self._setupGame()

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

    def testFixDevices(self):

        self._devices.getDevice(DeviceType.Phasers).damage       = BASIC_DAMAGE
        self._devices.getDevice(DeviceType.Phasers).deviceStatus = DeviceStatus.Damaged

        travelDistance: float = 3.162222
        warpFactor:     float = 5.0
        warpSquared: float = warpFactor ** 2
        elapsedTime: float = 10.0 * travelDistance / warpSquared
        self._gameState.opTime = elapsedTime

        self._eventEngine.fixDevices()

        repairedValue: float = BASIC_DAMAGE - elapsedTime

        repairedDevice: Device = self._devices.getDevice(DeviceType.Phasers)
        updatedFix:     float  = repairedDevice.damage

        self.assertAlmostEqual(first=repairedValue, second=updatedFix, msg="Not enough repair")

        self.logger.info(f"{repairedValue=} {updatedFix=}")

    def testFixDevicesNoOpTime(self):

        self._gameState.opTime = 0.0
        self._devices.getDevice(DeviceType.PhotonTubes).damage       = BASIC_DAMAGE
        self._devices.getDevice(DeviceType.PhotonTubes).deviceStatus = DeviceStatus.Damaged

        self._eventEngine.fixDevices()

        repairedDevice: Device = self._devices.getDevice(DeviceType.PhotonTubes)
        updatedFix:     float  = repairedDevice.damage

        self.assertEqual(first=BASIC_DAMAGE, second=updatedFix, msg="Should not have been repaired")
        self.logger.info(f"updatedFix: {updatedFix} {BASIC_DAMAGE=}")

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
        TestBase.resetSingletons()

        TestEventEngine.clsLogMessageConsole = LogMessageConsole()
        TestEventEngine.clsGameSettings      = GameSettings()     # Be able to read the preferences file
        TestEventEngine.clsIntelligence      = Intelligence()

        TestEventEngine.clsGameState         = GameState()        # Set up the game parameters which uses the above
        TestEventEngine.clsGameState.currentQuadrantCoordinates = TestEventEngine.clsIntelligence.generateQuadrantCoordinates()

        TestEventEngine.clsGameEngine        = GameEngine()       # Then the engine needs to be initialized

        TestEventEngine.clsEventEngine       = EventEngine(TestEventEngine.clsLogMessageConsole)
        TestEventEngine.clsDevices           = Devices()
        TestEventEngine.clsGalaxy            = Galaxy()


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestEventEngine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
