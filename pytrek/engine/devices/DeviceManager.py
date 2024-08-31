
from typing import Dict

from logging import Logger
from logging import getLogger


from codeallybasic.SingletonV3 import SingletonV3

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceStatus import DeviceStatus


class DeviceManager(metaclass=SingletonV3):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self.deviceMap:  Dict[DeviceType, Device] = {}

        for deviceType in DeviceType:

            device: Device = Device(deviceType=deviceType, deviceStatus=DeviceStatus.Up)
            self.deviceMap[deviceType] = device

        self.logger.debug(f"Created {len(self.deviceMap):3} devices")

    def fixDevices(self, starDate: float, opTime: float):
        # noinspection SpellCheckingInspection
        """
        // time taken by current operation
        double fintim = d.date + Time
        datemin = fintim;

        // d.date is current stardate

        xtime = datemin-d.date;

        repair = xtime;

        /* Don't fix Deathray here */
        for (l=1; l<=ndevice; l++)
            if (damage[l] > 0.0 && l != DDRAY)
                damage[l] -= (damage[l]-repair > 0.0 ? repair : damage[l]);

        /* Fix Deathray if docked */
        if (damage[DDRAY] > 0.0 && condit == IHDOCKED)
            damage[DDRAY] -= (damage[l] - xtime > 0.0 ? xtime : damage[DDRAY]);

        /* If radio repaired, update star chart and attack reports */

        """
        self.logger.info(f"Attempting to repair devices")
        finishTime:  float = starDate + opTime
        dateMinimum: float = finishTime
        extraTime:   float = dateMinimum - starDate
        repair:      float = extraTime

        for devType in DeviceType:
            device: Device = self.getDevice(devType)
            if device.deviceType != DeviceType.DeathRay:
                if device.damage > 0.0:
                    device.damage = device.damage - repair
                    if device.damage <= 0:
                        device.damage = 0
                        device.deviceStatus = DeviceStatus.Up
                        self.logger.info(f"Device: {device.deviceType.name} repaired")

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
