
from typing import Dict
from typing import List

from logging import Logger
from logging import getLogger

from re import Match as regExMatch
from re import search as regExSearch

from typing import NewType
from typing import cast

from arcade import key as arcadeKey

from pytrek.Constants import MAXIMUM_COORDINATE
from pytrek.Constants import MINIMUM_COORDINATE

from pytrek.commandparser.CommandType import CommandType
from pytrek.commandparser.ManualMoveData import ManualMoveData
from pytrek.commandparser.ParsedCommand import ParsedCommand

from pytrek.commandparser.InvalidCommandException import InvalidCommandException
from pytrek.commandparser.InvalidCommandValueException import InvalidCommandValueException
from pytrek.model.Coordinates import Coordinates

PressedKeyToCharacter: Dict[int, str] = {
    arcadeKey.A: 'a',
    arcadeKey.B: 'b',
    arcadeKey.C: 'c',
    arcadeKey.D: 'd',
    arcadeKey.E: 'e',
    arcadeKey.F: 'f',
    arcadeKey.G: 'g',
    arcadeKey.H: 'h',
    arcadeKey.I: 'i',
    arcadeKey.J: 'j',
    arcadeKey.K: 'k',
    arcadeKey.L: 'l',
    arcadeKey.M: 'm',
    arcadeKey.N: 'n',
    arcadeKey.O: 'o',
    arcadeKey.P: 'p',
    arcadeKey.Q: 'q',
    arcadeKey.R: 'r',
    arcadeKey.S: 's',
    arcadeKey.T: 't',
    arcadeKey.U: 'u',
    arcadeKey.V: 'v',
    arcadeKey.W: 'w',
    arcadeKey.X: 'x',
    arcadeKey.Y: 'y',
    arcadeKey.Z: 'z',
    arcadeKey.NUM_0: '0',
    arcadeKey.NUM_1: '1',
    arcadeKey.NUM_2: '2',
    arcadeKey.NUM_3: '3',
    arcadeKey.NUM_4: '4',
    arcadeKey.NUM_5: '5',
    arcadeKey.NUM_6: '6',
    arcadeKey.NUM_7: '7',
    arcadeKey.NUM_8: '8',
    arcadeKey.NUM_9: '9',
    arcadeKey.SPACE:  ' ',
    arcadeKey.ENTER:  '',
    arcadeKey.RETURN: '',
}

CommandPattern = NewType('CommandPattern', str)

REST_CMD:    CommandPattern = CommandPattern('^r |^rest ')
PHASERS_CMD: CommandPattern = CommandPattern('^p |^phasers ')
PHOTONS_CMD: CommandPattern = CommandPattern('^pho |^photons ')
WARP_CMD:    CommandPattern = CommandPattern('w |^warp ')
MOVE_CMD:    CommandPattern = CommandPattern('^m |^move ')

# These are 'move' subcommands
MOVE_MANUAL_MODE_PATTERN:    str = '^m|^manual'
MOVE_AUTOMATIC_MODE_PATTERN: str = 'a|^auto|^automatic'


PatternToCommandType: Dict[CommandPattern, CommandType] = {
    REST_CMD:    CommandType.Rest,
    PHASERS_CMD: CommandType.Phasers,
    PHOTONS_CMD: CommandType.Photons,
    WARP_CMD:    CommandType.Warp,
    MOVE_CMD:    CommandType.Move,
}


class CommandExtractor:
    """

    """
    def __init__(self):
        self.logger:      Logger = getLogger(__name__)
        self._commandStr: str    = ''

    def processKeyPress(self, pressedKey: int) -> ParsedCommand:

        self._commandStr = f'{self._commandStr}{PressedKeyToCharacter[pressedKey]}'

        if pressedKey == arcadeKey.ENTER or pressedKey == arcadeKey.RETURN:
            parsedCommand: ParsedCommand = self._parseCommand()
        else:
            parsedCommand = ParsedCommand(commandType=CommandType.NoCommand)

        return parsedCommand

    def _parseCommand(self) -> ParsedCommand:

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
                    pass
                elif len(splitCmd) == 4:    # sector coordinates only
                    parsedCommand.automaticMoveData.sectorCoordinates = self._parseSectorCoordinates(sRow=splitCmd[2], sColumn=splitCmd[3])
                else:
                    raise InvalidCommandException(message='Move automatic command improperly specified')
        else:
            manualMoveData: ManualMoveData = self._parseManualMoveSubcommand(splitCmd)
            parsedCommand.manualMoveData = manualMoveData

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
            manualMoveData.deltaX = int(splitCmd[2])
            manualMoveData.deltaY = int(splitCmd[3])
        except ValueError as e:
            self.logger.error(f'{e=}')
            raise InvalidCommandValueException(message=f'Invalid manual move values: {e}')

        return manualMoveData

    def _parseSectorCoordinates(self, sRow: str, sColumn: str) -> Coordinates:

        xCoordinate: int = -1
        yCoordinate: int = -1
        if (self._validCoordinate(coordinate=sRow, errorMsg='Invalid X sector') is True and
                self._validCoordinate(coordinate=sColumn, errorMsg='Invalid Y Sector') is True):
            xCoordinate = int(sRow)
            yCoordinate = int(sColumn)

        return Coordinates(x=xCoordinate, y=yCoordinate)

    def _validCoordinate(self, coordinate: str, errorMsg: str):
        """

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
