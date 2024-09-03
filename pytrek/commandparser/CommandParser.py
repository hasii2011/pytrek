
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
from pytrek.commandparser.ManualMoveData import ManualMoveType
from pytrek.commandparser.ParsedCommand import ParsedCommand
from pytrek.commandparser.InvalidCommandException import InvalidCommandException
from pytrek.commandparser.InvalidCommandValueException import InvalidCommandValueException
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.model.Coordinates import Coordinates

from pytrek.settings.GameSettings import GameSettings

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
DOCK_CMD:    CommandPattern = CommandPattern('^d|^dock')
SAVE_CMD:    CommandPattern = CommandPattern('^sa|^save')
LOAD_CMD:    CommandPattern = CommandPattern('^lo|^load')
#
# The following is for debugging events;  Requires that the debugEvents key
# in GameSettings (pytrek.ini) be set to 'True'
#
EVENT_CMD:    CommandPattern = CommandPattern('^event -')

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
    DOCK_CMD:    CommandType.Dock,
    SAVE_CMD:    CommandType.Save,
    EVENT_CMD:   CommandType.Event,
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

        self._gameSettings: GameSettings = GameSettings()

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
            case CommandType.Dock:
                pass            # nothing else to do
            case CommandType.Save:
                pass            # nothing else to do
            case CommandType.Event:
                if self._gameSettings.debugEvents is True:
                    self._parseEventCommand(parsedCommand=parsedCommand)
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
                raise InvalidCommandException(message='Move subcommand must be Manual or Automatic')
            else:

                if len(splitCmd) == 6:      # full auto command
                    parsedCommand.automaticMoveData.quadrantCoordinates = self._parseCoordinates(potentialX=splitCmd[2], potentialY=splitCmd[3])
                    parsedCommand.automaticMoveData.sectorCoordinates   = self._parseCoordinates(potentialX=splitCmd[4], potentialY=splitCmd[5])
                    parsedCommand.automaticMoveData.sectorMove = False
                elif len(splitCmd) == 4:    # sector coordinates only
                    parsedCommand.automaticMoveData.sectorCoordinates = self._parseCoordinates(potentialX=splitCmd[2], potentialY=splitCmd[3])
                else:
                    raise InvalidCommandException(message='Move command improperly specified')
                parsedCommand.manualMove = False
        else:
            manualMoveData: ManualMoveData = self._parseManualMoveSubcommand(splitCmd)
            parsedCommand.manualMoveData = manualMoveData
            parsedCommand.manualMove = True

            assert manualMoveData.moveType != ManualMoveType.NotSet, f'Should be either {ManualMoveType.QuadrantMove} or {ManualMoveType.SectorMove}'

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

    def _parseEventCommand(self, parsedCommand: ParsedCommand) -> ParsedCommand:

        self.logger.info(f'{parsedCommand=}')
        splitCmd:  List[str] = self._commandStr.split('-')
        eventName: str       = splitCmd[1].title().strip()
        try:
            eventType: FutureEventType = FutureEventType(eventName)
            parsedCommand.eventToTrigger = eventType
        except Exception as e:
            self.logger.error(f'{e=}')

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
        except ValueError:
            # self.logger.error(f'{errorMessage}: {e=}')
            raise InvalidCommandValueException(message=errorMessage)

        return integerValue

    def _parseManualMoveSubcommand(self, splitCmd: List[str]) -> ManualMoveData:
        """
        Manual move commands examples:

        m m -.1         Quadrant move 1 sector left
        m m -.1 .1      Quadrant move 1 sector left, and 1 sector down
        m m 1           Move 1 quadrant right
        m m -1 -1       Move 1 quadrant left and 1 quadrant up

        Args:
            splitCmd:

        Returns:
        """

        manualMoveData: ManualMoveData = ManualMoveData()
        try:
            manualMoveData.deltaX = float(splitCmd[2])
            if len(splitCmd) == 4:
                manualMoveData.deltaY = float(splitCmd[3])
            manualMoveData = self._determineManualMoveType(manualMoveData)

        except ValueError as e:
            self.logger.error(f'{e=}')
            raise InvalidCommandValueException(message=f'Invalid manual move values: {e}')

        return manualMoveData

    def _parseCoordinates(self, potentialX: str, potentialY: str) -> Coordinates:
        """

        Args:
            potentialX:
            potentialY:

        Returns: Valid coordinates or passes through an exception from validation
        """

        xCoordinate: int = -1
        yCoordinate: int = -1
        if (self._validCoordinate(coordinate=potentialX, errorMsg='Invalid X Coordinate') is True and
                self._validCoordinate(coordinate=potentialY, errorMsg='Invalid Y Coordinate') is True):
            xCoordinate = int(potentialX)
            yCoordinate = int(potentialY)

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
                raise InvalidCommandValueException(message=f'{errorMsg} bad coordinate {intCoordinate} {MINIMUM_COORDINATE=} {MAXIMUM_COORDINATE=}')

        except ValueError as e:
            self.logger.error(f'{e}')
            raise InvalidCommandValueException(message=errorMsg)

        return valid

    def _determineManualMoveType(self, manualMoveData: ManualMoveData) -> ManualMoveData:

        deltaX: float = manualMoveData.deltaX
        deltaY: float = manualMoveData.deltaY
        if self._inSectorRange(deltaX) and self._inSectorRange(deltaY) is True:
            manualMoveData.moveType = ManualMoveType.SectorMove
        else:
            manualMoveData.moveType = ManualMoveType.QuadrantMove

        return manualMoveData

    def _inSectorRange(self, deltaValue: float) -> bool:

        inRange: bool = False
        if -0.1 <= deltaValue <= 0.9:
            inRange = True

        return inRange
