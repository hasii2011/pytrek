
from typing import Dict

from logging import Logger
from logging import getLogger


from codeallybasic.Singleton import Singleton

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceStatus import DeviceStatus


class Devices(Singleton):

    # noinspection PyAttributeOutsideInit
    def init(self, *args, **kwargs):

        self.logger: Logger = getLogger(__name__)

        self.deviceMap: Dict[DeviceType, Device] = {}

        for deviceType in DeviceType:

            device: Device = Device(deviceType=deviceType, deviceStatus=DeviceStatus.Up)
            self.deviceMap[deviceType] = device

        self.logger.debug(f"Created {len(self.deviceMap):3} devices")

    def getDevice(self, deviceType: DeviceType):

        return self.deviceMap[deviceType]

    def getDeviceStatus(self, deviceType: DeviceType) -> DeviceStatus:
        return self.deviceMap[deviceType].deviceStatus

    def setDeviceStatus(self, deviceType: DeviceType, deviceStatus: DeviceStatus):

        self.logger.debug(f"set status deviceType: {deviceType}, deviceStatus: {deviceStatus}")
        self.deviceMap[deviceType].deviceStatus = deviceStatus

    def getDeviceDamage(self, deviceType: DeviceType) -> float:
        return self.deviceMap[deviceType].damage

    def setDeviceDamage(self, deviceType: DeviceType, damageValue: float):

        self.logger.debug(f"set damage deviceType: {deviceType}, damageValue: {damageValue}")
        self.deviceMap[deviceType].damage = damageValue

    def __repr__(self):

        myRep = "\n"
        for deviceType, device in self.deviceMap.items():
            devRep = (
                f"deviceType: {deviceType:27} "
                f"deviceStatus: {device.deviceStatus:7} "
                f"damage: {device.damage:4.4} \n"
            )
            myRep += devRep
        return myRep
