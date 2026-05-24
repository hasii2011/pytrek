
from enum import Enum


class GameType(Enum):
    """
    Use for computations involving game difficulty and length
    """
    Short  = 8
    Medium = 16
    Long   = 32

    @classmethod
    def toEnum(cls, strValue: str) -> 'GameType':

        match strValue:
            case 'Short':
                playerType: GameType = GameType.Short
            case 'Medium':
                playerType = GameType.Medium
            case 'Long':
                playerType = GameType.Long
            case _:
                raise Exception(f'Bad enumeration {strValue}')

        return playerType
