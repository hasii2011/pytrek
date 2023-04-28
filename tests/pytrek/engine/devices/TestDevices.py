
from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType

from tests.TestBase import TestBase

from pytrek.engine.devices.Devices import Devices


class TestDevices(TestBase):
    """
    """

    def testGetDevice(self):

        devices: Devices = Devices()

        testDevice: Device = devices.getDevice(DeviceType.DeathRay)

        self.assertEqual(first=testDevice.deviceType, second=DeviceType.DeathRay, msg='Got wrong device')

    def testSetDeviceStatus(self):

        devices: Devices = Devices()
        devices.setDeviceStatus(deviceType=DeviceType.LifeSupport, deviceStatus=DeviceStatus.Damaged)

        lifeSupport: Device = devices.getDevice(DeviceType.LifeSupport)

        self.assertEqual(first=lifeSupport.deviceStatus, second=DeviceStatus.Damaged, msg='Device did not change status')

        devices.setDeviceStatus(deviceType=DeviceType.LifeSupport, deviceStatus=DeviceStatus.Down)

        lf2: Device = devices.getDevice(DeviceType.LifeSupport)

        self.assertEqual(first=lf2.deviceStatus, second=DeviceStatus.Down, msg='Status did not change')

    def testDevicesRepr(self):

        # device:  Device  = Device(deviceType=DeviceType.DeathRay, deviceStatus=DeviceStatus.Damaged, initialDamage=42.42)
        # self.logger.info(f"device: {device}")

        devices: Devices = Devices()
        self.logger.info(f"devices: {devices}")


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDevices))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
