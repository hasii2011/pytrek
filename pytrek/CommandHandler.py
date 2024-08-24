
from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from pytrek.commandparser.CommandParser import CommandParser
from pytrek.commandparser.ManualMoveData import ManualMoveData
from pytrek.commandparser.ParsedCommand import ParsedCommand
from pytrek.commandparser.CommandType import CommandType
from pytrek.commandparser.InvalidCommandException import InvalidCommandException

from pytrek.gui.HelpView import HelpView

from pytrek.mediators.EnterpriseMediator import EnterpriseMediator
from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.engine.GameEngine import GameEngine

from pytrek.model.Coordinates import Coordinates

from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.GameState import GameState

if TYPE_CHECKING:
    from pytrek.PyTrekV2 import PyTrekV2


class CommandHandler:
    def __init__(self, view: 'PyTrekV2'):

        self.logger: Logger = getLogger(__name__)

        self._view:               'PyTrekV2'         = view
        self._commandParser:      CommandParser      = CommandParser()
        self._quadrantMediator:   QuadrantMediator   = QuadrantMediator()
        self._gameState:          GameState          = GameState()
        self._gameEngine:         GameEngine         = GameEngine()
        self._galaxyMediator:     GalaxyMediator     = GalaxyMediator()
        self._galaxy:             Galaxy             = Galaxy()

        self._enterpriseMediator: EnterpriseMediator = cast(EnterpriseMediator, None)

    def _setEnterpriseMediator(self, newValue: EnterpriseMediator):
        self._enterpriseMediator = newValue

    # noinspection PyTypeChecker
    enterpriseMediator = property(fget=None, fset=_setEnterpriseMediator, doc='Set by the section UI')

    def doCommand(self, commandStr: str):

        parsedCommand: ParsedCommand = self._commandParser.parseCommand(commandStr=commandStr)

        quadrant: Quadrant = self._galaxy.currentQuadrant
        match parsedCommand.commandType:
            #     case CommandType.Rest:
            #         parsedCommand = self._parseRestCommand(parsedCommand=parsedCommand)
            case CommandType.Photons:
                self._quadrantMediator.fireEnterpriseTorpedoes(quadrant)
                self._gameEngine.resetOperationTime()
            case CommandType.Phasers:
                self._quadrantMediator.firePhasers(quadrant)
                self._gameEngine.resetOperationTime()
            case CommandType.Warp:
                self._gameState.warpFactor = parsedCommand.warpFactor
                self._view.messageConsoleSection.displayMessage(f'Warp factor set to: {self._gameState.warpFactor}')
            case CommandType.Move:
                self._doMove(quadrant, parsedCommand)
            case CommandType.Chart:
                self._view.galaxySection.enabled = True
                self._gameEngine.resetOperationTime()
            case CommandType.LongRangeScan:
                self._view.longRangeSensorScanSection.enabled = True
                self._gameEngine.resetOperationTime()
            case CommandType.Damages:
                self._view.deviceStatusSection.enabled = True
            case CommandType.Help:
                self._displayHelp()
            case CommandType.Dock:
                self._quadrantMediator.dock(quadrant)
                self._gameEngine.resetOperationTime()
            case CommandType.Save:
                self._saveGame()
            case _:
                self.logger.error(f'Invalid command: {commandStr}')
                raise InvalidCommandException(message=f'Invalid command: {commandStr}')

    def _doMove(self, quadrant: Quadrant, parsedCommand: ParsedCommand):

        if parsedCommand.manualMove is True:
            manualMoveData: ManualMoveData = parsedCommand.manualMoveData
            self._enterpriseMediator.manualMove(quadrant=quadrant, deltaX=manualMoveData.deltaX, deltaY=manualMoveData.deltaY)
        else:
            pass

    def _displayHelp(self):
        """
        We are not using a section for help.  Because in arcade 2.6.17 sections and the GUI
        widgets are incompatible.   3.0.0
        """

        helpView: HelpView = HelpView(completeCallback=self._switchViewBack)
        self._view.window.show_view(helpView)

    def _saveGame(self):
        self._gameState.saveState()
        self._view.messageConsoleSection.displayMessage('Game saved !!')

    def _switchViewBack(self):
        self._view.window.show_view(self._view)
