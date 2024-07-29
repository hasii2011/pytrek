
from typing import Dict
from typing import List

from logging import Logger
from logging import getLogger

from re import Match as regExMatch
from re import search as regExSearch

from dataclasses import dataclass

from enum import Enum
from typing import NewType
from typing import cast

from arcade import key as arcadeKey


class CommandType(Enum):
    Abandon   = 'Abandon'
    Chart     = 'Chart'
    Capture   = 'Capture'
    Call      = 'Call'      # (for help)
    Cloak     = 'Cloak'
    Computer  = 'Computer'
    Crystals  = 'Crystals'
    Damages   = 'Damages'
    DeathRay  = 'DeathRay'
    Destruct  = 'Destruct'
    Dock      = 'Dock'
    Freeze    = 'Freeze'
    Impulse   = 'Impulse'
    Mine      = 'Mine'
    Move      = 'Move'
    Orbit     = 'Orbit'
    Phasers   = 'Phasers'
    Photons   = 'Photons'
    Planets   = 'Planets'
    Probe     = 'Probe'
    Report    = 'Report'
    Request   = 'Request'
    Rest      = 'Rest'
    Quit      = 'Quit'
    Score     = 'Score'
    Sensors   = 'Sensors'
    Shields   = 'Shields'
    Shuttle   = 'Shuttle'
    Status    = 'Status'
    Warp      = 'Warp'
    Transport      = 'Transport'
    ShortScan      = 'ShortRangeScan'
    LongRangeScan  = 'LongRangeScan'
    EmergencyExit  = 'EmergencyExit'
    NoCommand      = 'NoCommand'
    InvalidCommand = 'InvalidCommand'


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
PHOTONS_CMD: CommandPattern = CommandPattern('pho |^photons ')


PatternToCommandType: Dict[CommandPattern, CommandType] = {
    REST_CMD:    CommandType.Rest,
    PHASERS_CMD: CommandType.Phasers,
    PHOTONS_CMD: CommandType.Photons,
}


@dataclass
class ParsedCommand:
    commandType: CommandType = CommandType.NoCommand

    restInterval:       int = 0
    phaserAmountToFire: int = 0


class CommandExtractor:

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
                try:
                    splitCmd:  List[str] = self._commandStr.split(' ')
                    parsedCommand.restInterval = int(splitCmd[1])
                    self._commandStr = ''
                except ValueError as e:
                    self.logger.error(f'{e=}')
                    parsedCommand.commandType = CommandType.InvalidCommand
            case CommandType.Phasers:
                try:
                    splitCmd = self._commandStr.split(' ')
                    parsedCommand.phaserAmountToFire = int(splitCmd[1])
                    self._commandStr = ''
                except ValueError as e:
                    self.logger.error(f'{e=}')
                    parsedCommand.commandType = CommandType.InvalidCommand
            case CommandType.Photons:
                pass        # TODO
            case _:
                self.logger.error(f'Invalid command: {self._commandStr}')
                parsedCommand.commandType = CommandType.InvalidCommand

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
