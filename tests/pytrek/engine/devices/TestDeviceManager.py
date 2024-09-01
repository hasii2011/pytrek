
from unittest import TestSuite

from unittest import main as unitTestMain

from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.ShipCondition import ShipCondition

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceManager import DeviceManager

from tests.ProjectTestBase import ProjectTestBase


BASIC_DAMAGE = 4.0


class TestDeviceManager(ProjectTestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        """"""
        super().setUpClass()
        ProjectTestBase.resetSingletons()

    def setUp(self):
        super().setUp()

        self._deviceManager: DeviceManager = DeviceManager()
        self._intelligence:  Intelligence  = Intelligence()

    def testGetDevice(self):

        devices: DeviceManager = DeviceManager()

        testDevice: Device = devices.getDevice(DeviceType.DeathRay)

        self.assertEqual(first=testDevice.deviceType, second=DeviceType.DeathRay, msg='Got wrong device')

    def testSetDeviceStatus(self):

        devices: DeviceManager = DeviceManager()
        devices.setDeviceStatus(deviceType=DeviceType.LifeSupport, deviceStatus=DeviceStatus.Damaged)

        lifeSupport: Device = devices.getDevice(DeviceType.LifeSupport)

        self.assertEqual(first=lifeSupport.deviceStatus, second=DeviceStatus.Damaged, msg='Device did not change status')

        devices.setDeviceStatus(deviceType=DeviceType.LifeSupport, deviceStatus=DeviceStatus.Down)

        lf2: Device = devices.getDevice(DeviceType.LifeSupport)

        self.assertEqual(first=lf2.deviceStatus, second=DeviceStatus.Down, msg='Status did not change')

    def testDevicesRepr(self):
        self.logger.info(f"Device Manager: {self._deviceManager}")

    def testFixDevices(self):

        self._deviceManager.getDevice(DeviceType.Phasers).damage       = BASIC_DAMAGE
        self._deviceManager.getDevice(DeviceType.Phasers).deviceStatus = DeviceStatus.Damaged

        travelDistance: float = 3.162222
        warpFactor:     float = 5.0
        warpSquared:    float = warpFactor ** 2
        elapsedTime:    float = 10.0 * travelDistance / warpSquared
        opTime:         float = elapsedTime
        starDate:       float = self._intelligence.generateInitialStarDate()

        self._deviceManager.fixDevices(opTime=opTime, starDate=starDate, shipCondition=ShipCondition.Green)

        repairedValue: float = BASIC_DAMAGE - elapsedTime

        repairedDevice: Device = self._deviceManager.getDevice(DeviceType.Phasers)
        updatedFix:     float  = repairedDevice.damage

        self.assertAlmostEqual(first=repairedValue, second=updatedFix, msg="Not enough repair")

        self.logger.info(f"{repairedValue=} {updatedFix=}")

    def testFixDevicesNoOpTime(self):

        opTime:   float = 0.0
        starDate: float = self._intelligence.generateInitialStarDate()

        self._deviceManager.getDevice(DeviceType.PhotonTubes).damage       = BASIC_DAMAGE
        self._deviceManager.getDevice(DeviceType.PhotonTubes).deviceStatus = DeviceStatus.Damaged

        self._deviceManager.fixDevices(opTime=opTime, starDate=starDate, shipCondition=ShipCondition.Green)

        repairedDevice: Device = self._deviceManager.getDevice(DeviceType.PhotonTubes)
        updatedFix:     float  = repairedDevice.damage

        self.assertEqual(first=BASIC_DAMAGE, second=updatedFix, msg="Should not have been repaired")
        self.logger.info(f"updatedFix: {updatedFix} {BASIC_DAMAGE=}")

    def testFixDeathRayNotDockedNotFixed(self):

        self._deviceManager.getDevice(DeviceType.DeathRay).damage       = BASIC_DAMAGE
        self._deviceManager.getDevice(DeviceType.DeathRay).deviceStatus = DeviceStatus.Damaged

        opTime:   float = 2
        starDate: float = self._intelligence.generateInitialStarDate()

        self._deviceManager.fixDevices(opTime=opTime, starDate=starDate, shipCondition=ShipCondition.Green)

        self.assertEqual(BASIC_DAMAGE, self._deviceManager.getDevice(DeviceType.DeathRay).damage, 'Should not be fixable')

    def testFixDeathRayDockedAndFixed(self):

        self._deviceManager.getDevice(DeviceType.DeathRay).damage       = BASIC_DAMAGE
        self._deviceManager.getDevice(DeviceType.DeathRay).deviceStatus = DeviceStatus.Damaged

        opTime:   float = 2
        starDate: float = self._intelligence.generateInitialStarDate()

        self._deviceManager.fixDevices(opTime=opTime, starDate=starDate, shipCondition=ShipCondition.Docked)

        self.assertEqual(BASIC_DAMAGE - opTime, self._deviceManager.getDevice(DeviceType.DeathRay).damage, 'Should be fixable')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDeviceManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
