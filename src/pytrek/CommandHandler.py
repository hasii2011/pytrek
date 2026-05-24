
from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from pytrek.Constants import CRITICAL_WARP_ENGINE_DAMAGE
from pytrek.Constants import MAXIMUM_DAMAGED_WARP_FACTOR

from pytrek.commandparser.AutomaticMoveData import AutomaticMoveData
from pytrek.commandparser.CommandParser import CommandParser
from pytrek.commandparser.ManualMoveData import ManualMoveData
from pytrek.commandparser.ManualMoveData import ManualMoveType
from pytrek.commandparser.ParsedCommand import ParsedCommand
from pytrek.commandparser.CommandType import CommandType
from pytrek.commandparser.InvalidCommandException import InvalidCommandException

from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceManager import DeviceManager

from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.mediators.EnterpriseMediator import EnterpriseMediator
from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.gui.HelpView import HelpView

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
        self._deviceManager:      DeviceManager      = DeviceManager()
        self._eventEngine:        EventEngine        = EventEngine()

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
                self._setWarpFactor(parsedCommand=parsedCommand)
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
            case CommandType.Event:
                self._triggerEvent(parsedCommand.eventToTrigger)
            case CommandType.Save:
                self._saveGame()
            case _:
                self.logger.error(f'Invalid command: {commandStr}')
                raise InvalidCommandException(message=f'Invalid command: {commandStr}')

    def _setWarpFactor(self, parsedCommand: ParsedCommand):

        warpEngineDamage: float = self._deviceManager.getDeviceDamage(deviceType=DeviceType.WarpEngines)
        warpFactor:       int   = parsedCommand.warpFactor

        if warpEngineDamage > CRITICAL_WARP_ENGINE_DAMAGE:
            self._view.messageConsoleSection.displayMessage("Engineer Scott- \"The warp engines are damaged, Sir.\"")
        elif warpEngineDamage > 0.0 and warpFactor > MAXIMUM_DAMAGED_WARP_FACTOR:
            self._view.messageConsoleSection.displayMessage("Engineer Scott- \"Sorry, Captain. Until this damage")
            self._view.messageConsoleSection.displayMessage("  is repaired, I can only give you warp 4.\"")
        else:
            self._gameState.warpFactor = warpFactor
            self._view.messageConsoleSection.displayMessage(f'Warp factor set to: {self._gameState.warpFactor}')

    def _doMove(self, quadrant: Quadrant, parsedCommand: ParsedCommand):

        if parsedCommand.manualMove is True:
            manualMoveData: ManualMoveData = parsedCommand.manualMoveData
            inSectorMove: bool = False
            if manualMoveData.moveType == ManualMoveType.SectorMove:
                inSectorMove = True

            self._enterpriseMediator.manualMove(quadrant=quadrant, deltaX=manualMoveData.deltaX, deltaY=manualMoveData.deltaY, inSectorMove=inSectorMove)
        else:
            assert parsedCommand.manualMove is False, 'Cannot assume it is automatic'
            moveData: AutomaticMoveData = parsedCommand.automaticMoveData
            self._enterpriseMediator.automaticMove(quadrantCoordinates=moveData.quadrantCoordinates, sectorCoordinates=moveData.sectorCoordinates)

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

    def _triggerEvent(self, eventToTrigger: FutureEventType):
        self._eventEngine.debugFireEvent(eventType=eventToTrigger)

    def _switchViewBack(self):
        self._view.window.show_view(self._view)
