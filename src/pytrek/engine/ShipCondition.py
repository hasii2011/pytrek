
from enum import Enum


class ShipCondition(Enum):

    Green   = 'Green'
    Yellow  = 'Yellow'
    Red     = 'Red'
    Docked  = 'Docked'
    Dead    = 'Dead'

    def __str__(self):
        return self.name
