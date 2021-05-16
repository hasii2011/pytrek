
from enum import Enum


class DeviceStatus(Enum):
    """
        Describes the possible device statuses;  Or is that stati ;=)
    """
    Down    = 0
    Up      = 1
    Damaged = 3

    def __str__(self):
        return str(self.name)
