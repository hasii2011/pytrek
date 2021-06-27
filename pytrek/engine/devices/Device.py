
from typing import cast

from dataclasses import dataclass

from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceStatus import DeviceStatus


@dataclass
class Device:

    deviceType:   DeviceType   = cast(DeviceType, None)
    deviceStatus: DeviceStatus = cast(DeviceStatus, None)
    damage:       float        = 0.0

    def __repr__(self):

        myRep = f"deviceType: {self.deviceType} deviceStatus: {self.deviceStatus} damage: {self.damage}"
        return myRep
