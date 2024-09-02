
from dataclasses import dataclass

from enum import Enum


class ManualMoveType(Enum):
    SectorMove   = 'SectorMove'
    QuadrantMove = 'QuadrantMove'
    NotSet       = 'NotSet'


@dataclass
class ManualMoveData:
    """
    Less than 1 positive and negative values should be processed as moves within the quadrants (e.g. .1 .1)
    greater than one moves are deltas within the galaxy
    """
    moveType: ManualMoveType = ManualMoveType.NotSet
    deltaX: float = 0.0
    deltaY: float = 0.0
