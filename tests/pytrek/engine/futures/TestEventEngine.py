

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.GameEngine import GameEngine

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices

from pytrek.engine.futures.EventEngine import EventEngine

from pytrek.settings.SettingsCommon import SettingsCommon

from pytrek.GameState import GameState

from tests.TestBase import TestBase
from tests.pytrek.engine.futures.LogMessageConsole import LogMessageConsole

BASIC_DAMAGE = 4.0


class TestEventEngine(TestBase):
    """"""
    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        """"""
        self.logger:      Logger      = getLogger(__name__)
        #
        # The game engine initializes the game state object (for better or worse)
        #
        self._gameEngine:  GameEngine  = GameEngine()
        self._gameState:   GameState   = GameState()
        self._eventEngine: EventEngine = EventEngine(LogMessageConsole())
        self._devices:     Devices     = Devices()

    def testCheckEvents(self):
        pass

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


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestEventEngine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
