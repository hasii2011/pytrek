
from enum import Enum


class SoundVolume(Enum):

    Low    = 0.1
    Medium = 0.5
    High   = 1.0

    @classmethod
    def toEnum(cls, strValue: str) -> 'SoundVolume':

        match strValue:
            case 'Low':
                soundVolume: SoundVolume = SoundVolume.Low
            case 'Medium':
                soundVolume = SoundVolume.Medium
            case 'High':
                soundVolume = SoundVolume.High
            case _:
                raise Exception(f'Bad enumeration {strValue}')

        return soundVolume
