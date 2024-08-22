
from typing import Dict
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from re import Match as regExMatch
from re import search as regExSearch

from pytrek.Constants import MAXIMUM_COORDINATE
from pytrek.Constants import MINIMUM_COORDINATE

from pytrek.commandparser.CommandType import CommandType
from pytrek.commandparser.ManualMoveData import ManualMoveData
from pytrek.commandparser.ParsedCommand import ParsedCommand

from pytrek.commandparser.InvalidCommandException import InvalidCommandException
from pytrek.commandparser.InvalidCommandValueException import InvalidCommandValueException
from pytrek.model.Coordinates import Coordinates

CommandPattern = NewType('CommandPattern', str)

REST_CMD:    CommandPattern = CommandPattern('^r |^rest ')
PHASERS_CMD: CommandPattern = CommandPattern('^p |^phasers ')
PHOTONS_CMD: CommandPattern = CommandPattern('^pho |^photons ')
WARP_CMD:    CommandPattern = CommandPattern('w |^warp ')
MOVE_CMD:    CommandPattern = CommandPattern('^m |^move ')
LRSCAN_CMD:  CommandPattern = CommandPattern('^l|^lrscan')
DAMAGES_CMD: CommandPattern = CommandPattern('^da|^damages')
CHART_CMD:   CommandPattern = CommandPattern('^c|^chart')
HELP_CMD:    CommandPattern = CommandPattern('^help')

# These are 'move' subcommands
MOVE_MANUAL_MODE_PATTERN:    str = '^m|^manual'
MOVE_AUTOMATIC_MODE_PATTERN: str = 'a|^auto|^automatic'


PatternToCommandType: Dict[CommandPattern, CommandType] = {
    REST_CMD:    CommandType.Rest,
    PHASERS_CMD: CommandType.Phasers,
    PHOTONS_CMD: CommandType.Photons,
    WARP_CMD:    CommandType.Warp,
    MOVE_CMD:    CommandType.Move,
    LRSCAN_CMD:  CommandType.LongRangeScan,
    DAMAGES_CMD: CommandType.Damages,
    CHART_CMD:   CommandType.Chart,
    HELP_CMD:    CommandType.Help,
}


class CommandParser:
    """
    This classes processes (eats) keystrokes until the player presses the `Enter` key.  These are
    cached in `_commandStr`.  At that point, `_parseCommand` runs a series of regular expressions
    to determine which command the player input.  If it cannot find a matching command `_parsedCommand`
    throws an `InvalidCommandException`.

    The various `_parseXXXCommand` methods may throw an `InvalidCommandValueException` if the command values
    are invalid.  For example, inputting non-numeric input to the `rest` command or inputting an
    invalid coordinate pair to the `move`

    The `move` may also throw an `InvalidCommandException` if its subcommand is not valid.

    """
    def __init__(self, asciiMode: bool = False):
        self.logger:      Logger = getLogger(__name__)

        self._asciiMode:  bool   = asciiMode
        self._commandStr: str    = ''

    def parseCommand(self, commandStr: str) -> ParsedCommand:

        self._commandStr = commandStr.lower()
        parsedCommand = self._matchCommand(commandStr=self._commandStr)
        match parsedCommand.commandType:
            case CommandType.Rest:
                parsedCommand = self._parseRestCommand(parsedCommand=parsedCommand)
            case CommandType.Phasers:
                parsedCommand = self._parsePhasersCommand(parsedCommand=parsedCommand)
            case CommandType.Photons:
                parsedCommand = self._parsePhotonsCommand(parsedCommand=parsedCommand)
            case CommandType.Warp:
                parsedCommand = self._parseWarpCommand(parsedCommand=parsedCommand)
            case CommandType.Move:
                parsedCommand = self._parseMoveCommand(parsedCommand=parsedCommand)
            case CommandType.Chart:
                pass            # nothing else to do
            case CommandType.LongRangeScan:
                pass            # nothing else to do
            case CommandType.Damages:
                pass            # nothing else to do
            case CommandType.Help:
                pass            # nothing else to do
            case _:
                self.logger.error(f'Invalid command: {self._commandStr}')
                raise InvalidCommandException(message=f'Invalid command: {self._commandStr}')

        return parsedCommand

    def _parseMoveCommand(self, parsedCommand: ParsedCommand):
        """
        move manual <deltaX> <deltaY>

        move automatic <qRow> <qColumn> <sRow> <sColumn>

        For moving within a quadrant, <qRow> and <qColumn> may be omitted

        Args:
            parsedCommand:
        """

        splitCmd: List[str] = self._commandStr.split(' ')

        modeStr: str = splitCmd[1]
        match: regExMatch | None = regExSearch(MOVE_MANUAL_MODE_PATTERN, modeStr)
        if match is None:
            match = regExSearch(MOVE_AUTOMATIC_MODE_PATTERN, modeStr)
            if match is None:
                raise InvalidCommandException(message='Move subcommand must be manual or auto')
            else:

                if len(splitCmd) == 6:      # full auto command
                    parsedCommand.automaticMoveData.quadrantCoordinates = self._parseCoordinates(sRow=splitCmd[2], sColumn=splitCmd[3])
                    parsedCommand.automaticMoveData.sectorCoordinates   = self._parseCoordinates(sRow=splitCmd[4], sColumn=splitCmd[5])
                    parsedCommand.automaticMoveData.sectorMove = False
                elif len(splitCmd) == 4:    # sector coordinates only
                    parsedCommand.automaticMoveData.sectorCoordinates = self._parseCoordinates(sRow=splitCmd[2], sColumn=splitCmd[3])
                else:
                    raise InvalidCommandException(message='Move automatic command improperly specified')
        else:
            manualMoveData: ManualMoveData = self._parseManualMoveSubcommand(splitCmd)
            parsedCommand.manualMoveData = manualMoveData
            parsedCommand.manualMove     = True

        return parsedCommand

    def _parseRestCommand(self, parsedCommand: ParsedCommand) -> ParsedCommand:
        """
        Retrieve the rest interval
        Args:
            parsedCommand:   command to update

        Returns:  Updated command
        """
        parsedCommand.restInterval = self._getSingleIntegerValue(self._commandStr, errorMessage='Bad rest value')
        return parsedCommand

    def _parsePhasersCommand(self, parsedCommand: ParsedCommand) -> ParsedCommand:
        """
        Retrieve the amount to fire
        Args:
            parsedCommand:  Command to update

        Returns: The updated command
        """
        parsedCommand.phaserAmountToFire = self._getSingleIntegerValue(self._commandStr, errorMessage='Bad phaser power value')
        return parsedCommand

    def _parsePhotonsCommand(self, parsedCommand: ParsedCommand) -> ParsedCommand:
        """
        Retrieve the number of torpedoes to fire
        Args:
            parsedCommand:  Command to update

        Returns:  The updated command
        """
        parsedCommand.numberOfPhotonTorpedoesToFire = self._getSingleIntegerValue(self._commandStr, errorMessage='Bad photon count')
        return parsedCommand

    def _parseWarpCommand(self, parsedCommand: ParsedCommand) -> ParsedCommand:

        parsedCommand.warpFactor = self._getSingleIntegerValue(self._commandStr, errorMessage='Invalid warp factor')

        return parsedCommand

    def _matchCommand(self, commandStr: str) -> ParsedCommand:
        """
        Loop through the regular expression dictionary attempting to find a match
        Args:
            commandStr: The full captured command text

        Returns:  The parsed command with the correct command type or a pass through exception
        """

        parsedCommand: ParsedCommand = ParsedCommand(commandType=CommandType.NoCommand)

        for pattern in PatternToCommandType.keys():
            cmdPattern: CommandPattern    = cast(CommandPattern, pattern)
            match:      regExMatch | None = regExSearch(cmdPattern, commandStr)

            if match is not None:
                parsedCommand.commandType = PatternToCommandType[cmdPattern]
                break

        return parsedCommand

    def _getSingleIntegerValue(self, commandStr: str, errorMessage: str) -> int:

        try:
            splitCmd:     List[str] = commandStr.split(' ')
            integerValue: int       = int(splitCmd[1])
            self._commandStr = ''
        except ValueError as e:
            self.logger.error(f'{errorMessage}: {e=}')
            raise InvalidCommandValueException(message=errorMessage)

        return integerValue

    def _parseManualMoveSubcommand(self, splitCmd: List[str]) -> ManualMoveData:

        manualMoveData: ManualMoveData = ManualMoveData()
        try:
            manualMoveData.deltaX = float(splitCmd[2])
            if len(splitCmd) == 4:
                manualMoveData.deltaY = float(splitCmd[3])
        except ValueError as e:
            self.logger.error(f'{e=}')
            raise InvalidCommandValueException(message=f'Invalid manual move values: {e}')

        return manualMoveData

    def _parseCoordinates(self, sRow: str, sColumn: str) -> Coordinates:

        xCoordinate: int = -1
        yCoordinate: int = -1
        if (self._validCoordinate(coordinate=sRow, errorMsg='Invalid X Coordinate') is True and
                self._validCoordinate(coordinate=sColumn, errorMsg='Invalid Y Coordinate') is True):
            xCoordinate = int(sRow)
            yCoordinate = int(sColumn)

        return Coordinates(x=xCoordinate, y=yCoordinate)

    def _validCoordinate(self, coordinate: str, errorMsg: str):
        """
        TODO:  This is duplicated in the EnterpriseMediator

        Args:
            coordinate:  String coordinate
            errorMsg:    Error message to put in exception if not valid

        Returns:  True if coordinate is value;  Else raises exception

        """
        valid: bool = True

        try:
            intCoordinate: int = int(coordinate)
            if intCoordinate < MINIMUM_COORDINATE or intCoordinate > MAXIMUM_COORDINATE:
                raise InvalidCommandValueException(message=f'{errorMsg} {MINIMUM_COORDINATE=} {MAXIMUM_COORDINATE=}')

        except ValueError as e:
            self.logger.error(f'{e}')
            raise InvalidCommandValueException(message=errorMsg)

        return valid
