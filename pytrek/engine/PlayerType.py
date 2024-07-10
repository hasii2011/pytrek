
from enum import Enum


class PlayerType(Enum):
    """
    Use as a computation value to determine things like:
    * Length of game
    * Number of enemies
    * Initial Energy
    * Super Commander Count
    """
    Novice   = 1
    Fair     = 2
    Good     = 3
    Expert   = 4
    Emeritus = 5

    @classmethod
    def toEnum(cls, strValue: str) -> 'PlayerType':

        match strValue:
            case 'Novice':
                playerType: PlayerType = PlayerType.Novice
            case 'Fair':
                playerType = PlayerType.Fair
            case 'Good':
                playerType = PlayerType.Good
            case 'Expert':
                playerType = PlayerType.Expert
            case 'Emeritus':
                playerType = PlayerType.Emeritus
            case _:
                raise Exception(f'Bad enumeration {strValue}')

        return playerType
