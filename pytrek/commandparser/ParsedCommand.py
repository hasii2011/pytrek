
from dataclasses import dataclass
from dataclasses import field

from pytrek.commandparser.AutomaticMoveData import AutomaticMoveData
from pytrek.commandparser.CommandType import CommandType
from pytrek.commandparser.ManualMoveData import ManualMoveData


def manualMoveDataFactory() -> ManualMoveData:
    return ManualMoveData()


def automaticMoveDataFactory() -> AutomaticMoveData:
    return AutomaticMoveData()


@dataclass
class ParsedCommand:
    """
    Each command type has associated data.  You can tell which is which
    by looking at the command type names

    For the move sub commands (auto/manual) their associated data is only valid
    depending on the manual move flag
    """
    commandType: CommandType = CommandType.NoCommand

    restInterval:       int  = 0
    warpFactor:         int  = 0
    phaserAmountToFire: int  = 0
    manualMove:         bool = False

    manualMoveData:    ManualMoveData    = field(default_factory=manualMoveDataFactory)
    automaticMoveData: AutomaticMoveData = field(default_factory=automaticMoveDataFactory)

    numberOfPhotonTorpedoesToFire: int = 0
