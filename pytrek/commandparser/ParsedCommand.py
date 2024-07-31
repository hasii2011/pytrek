
from dataclasses import dataclass
from dataclasses import field

from pytrek.commandparser.CommandType import CommandType
from pytrek.commandparser.ManualMoveData import ManualMoveData


def manualMoveDataFactory() -> ManualMoveData:
    return ManualMoveData()


@dataclass
class ParsedCommand:
    commandType: CommandType = CommandType.NoCommand

    restInterval:       int = 0
    warpFactor:         int = 0
    phaserAmountToFire: int = 0

    manualMoveData: ManualMoveData = field(default_factory=manualMoveDataFactory)

    numberOfPhotonTorpedoesToFire: int = 0
