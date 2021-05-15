
from dataclasses import dataclass

from pytrek.engine.DeviceType import DeviceType
from pytrek.engine.DeviceStatus import DeviceStatus


@dataclass
class Device:

    deviceType:   DeviceType   = None
    deviceStatus: DeviceStatus = None
    damage:       float        = 0.0

    def __repr__(self):

        myRep = f"deviceType: {self.deviceType} deviceStatus: {self.deviceStatus} damage: {self.damage}"
        return myRep
