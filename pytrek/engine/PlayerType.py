
from enum import Enum


class PlayerType(Enum):
    """
    Use as a computation value to determine things like:
    * Length of game
    * Number of enemies
    * Initial Energy
    """
    Novice   = 1
    Fair     = 2
    Good     = 3
    Expert   = 4
    Emeritus = 5
