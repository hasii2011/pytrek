
from dataclasses import dataclass
from typing import List

from pytrek.engine.PlayerType import PlayerType


@dataclass
class TorpedoSpeeds:

    NUM_VALUES: int = 4

    playerType: PlayerType = PlayerType.Novice

    enterprise:     int = 0
    klingon:        int = 0
    commander:      int = 0
    superCommander: int = 0

    @classmethod
    def toTorpedoSpeed(cls, speedStr: str):
        """
        Assumes the input string is comma delimited in the form:

        enterprise,klingon,commander,super commander

        Args:
            speedStr:   In the above form

        Returns:  An appropriate speed object
        """
        tp: TorpedoSpeeds = TorpedoSpeeds()

        chunks: List[str] = speedStr.split(',')

        if len(chunks) != TorpedoSpeeds.NUM_VALUES:
            raise ValueError('Not an appropriate number of values')

        tp.enterprise = int(chunks[0])
        tp.klingon    = int(chunks[1])
        tp.commander  = int(chunks[2])
        tp.superCommander = int(chunks[3])

        return tp
