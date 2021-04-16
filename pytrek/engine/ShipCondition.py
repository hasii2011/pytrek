
from enum import Enum


class ShipCondition(Enum):

    Green   = 0
    Yellow  = 1
    Red     = 2
    Docked  = 3
    Dead    = 4

    def __str__(self):
        return self.name
