
from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType

from tests.ProjectTestBase import ProjectTestBase

from pytrek.engine.devices.DeviceManager import DeviceManager

BASIC_DAMAGE = 4.0


class TestDeviceManager(ProjectTestBase):
    """
    """
    def setUp(self):
        super().setUp()
        self._devices:     DeviceManager = DeviceManager()
        self._intelligence: Intelligence = Intelligence()

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

        # device:  Device  = Device(deviceType=DeviceType.DeathRay, deviceStatus=DeviceStatus.Damaged, initialDamage=42.42)
        # self.logger.info(f"device: {device}")

        devices: DeviceManager = DeviceManager()
        self.logger.info(f"devices: {devices}")

    def testFixDevices(self):

        self._devices.getDevice(DeviceType.Phasers).damage       = BASIC_DAMAGE
        self._devices.getDevice(DeviceType.Phasers).deviceStatus = DeviceStatus.Damaged

        travelDistance: float = 3.162222
        warpFactor:     float = 5.0
        warpSquared:    float = warpFactor ** 2
        elapsedTime:    float = 10.0 * travelDistance / warpSquared
        opTime:         float = elapsedTime
        starDate:       float = self._intelligence.generateInitialStarDate()

        self._devices.fixDevices(opTime=opTime, starDate=starDate)

        repairedValue: float = BASIC_DAMAGE - elapsedTime

        repairedDevice: Device = self._devices.getDevice(DeviceType.Phasers)
        updatedFix:     float  = repairedDevice.damage

        self.assertAlmostEqual(first=repairedValue, second=updatedFix, msg="Not enough repair")

        self.logger.info(f"{repairedValue=} {updatedFix=}")

    def testFixDevicesNoOpTime(self):

        opTime:   float = 0.0
        starDate: float = self._intelligence.generateInitialStarDate()

        self._devices.getDevice(DeviceType.PhotonTubes).damage       = BASIC_DAMAGE
        self._devices.getDevice(DeviceType.PhotonTubes).deviceStatus = DeviceStatus.Damaged

        self._devices.fixDevices(opTime=opTime, starDate=starDate)

        repairedDevice: Device = self._devices.getDevice(DeviceType.PhotonTubes)
        updatedFix:     float  = repairedDevice.damage

        self.assertEqual(first=BASIC_DAMAGE, second=updatedFix, msg="Should not have been repaired")
        self.logger.info(f"updatedFix: {updatedFix} {BASIC_DAMAGE=}")


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDeviceManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
