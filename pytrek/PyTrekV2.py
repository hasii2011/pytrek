
from typing import cast

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from PIL import ImageFont

from arcade import Texture
from arcade import View
from arcade import Window

from arcade import run as arcadeRun

from arcade import start_render

from pytrek.CommandHandler import CommandHandler
from pytrek.GameState import GameState
from pytrek.LocateResources import LocateResources

from pytrek.Constants import COMMAND_SECTION_HEIGHT
from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_FILENAME
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.Constants import STATUS_VIEW_WIDTH

from pytrek.commandparser.InvalidCommandException import InvalidCommandException
from pytrek.commandparser.InvalidCommandValueException import InvalidCommandValueException

from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.gui.ConsoleMessageType import ConsoleMessageType
from pytrek.gui.DeviceStatusSection import DeviceStatusSection
from pytrek.gui.GalaxySection import GalaxySection
from pytrek.gui.LongRangeSensorScanSection import LongRangeSensorScanSection
from pytrek.gui.MessageConsoleProxy import MessageConsoleProxy
from pytrek.gui.MessageConsoleSection import MessageConsoleSection
from pytrek.gui.QuadrantSection import QuadrantSection
from pytrek.gui.StatusConsoleSection import StatusConsoleSection
from pytrek.gui.VatoLocoTextSection import VatoLocoTextSection
from pytrek.gui.WarpEffectSection import WarpEffectSection
from pytrek.gui.gamepieces.Enterprise import Enterprise

from pytrek.mediators.EnterpriseMediator import EnterpriseMediator
from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings

SCREEN_TITLE:  str = "PyTrekV2"


class PyTrekV2(View):

    def __init__(self):

        LocateResources.setupSystemLogging()

        self.logger: Logger = getLogger(__name__)
        super().__init__()

        self.background:  Texture    = cast(Texture, None)
        self._enterprise: Enterprise = cast(Enterprise, None)

        self._intelligence: Intelligence             = cast(Intelligence, None)
        self._computer:     Computer                 = cast(Computer, None)
        self._gameEngine:   GameEngine               = cast(GameEngine, None)
        self._gameState:    GameState                = cast(GameState, None)
        self._gameSettings: GameSettings             = cast(GameSettings, None)
        self._galaxy:       Galaxy                   = cast(Galaxy, None)
        self._quadrant:     Quadrant                 = cast(Quadrant, None)

        self._quadrantMediator:   QuadrantMediator   = cast(QuadrantMediator, None)
        self._galaxyMediator:     GalaxyMediator     = cast(GalaxyMediator, None)

        self.messageConsoleSection:      MessageConsoleSection      = cast(MessageConsoleSection, None)
        self._messageConsoleProxy:       MessageConsoleProxy        = cast(MessageConsoleProxy, None)
        self._statusConsole:             StatusConsoleSection       = cast(StatusConsoleSection, None)
        self._quadrantSection:           QuadrantSection            = cast(QuadrantSection, None)
        self._commandInputSection:       VatoLocoTextSection        = cast(VatoLocoTextSection, None)
        self.galaxySection:              GalaxySection              = cast(GalaxySection, None)
        self.longRangeSensorScanSection: LongRangeSensorScanSection = cast(LongRangeSensorScanSection, None)

        self._enterpriseMediator: EnterpriseMediator = cast(EnterpriseMediator, None)
        self._setupGame()
        self._setupUI()
        self._enterpriseMediator.warpEffectSection = self.warpEffectSection

        self._commandHandler:     CommandHandler = CommandHandler(view=self)
        self._commandHandler.enterpriseMediator  = self._enterpriseMediator

    def on_draw(self):
        start_render()

    def _setupGame(self):
        """
        We need to set up the game singletons in the correct order.  Do this here
        """
        #
        # I am cheating here because I know arcade uses PIL under the covers
        #
        fqFileName: str = LocateResources.getResourcesPath(bareFileName=FIXED_WIDTH_FONT_FILENAME,
                                                           resourcePath=LocateResources.FONT_RESOURCES_PATH,
                                                           packageName=LocateResources.FONT_RESOURCES_PACKAGE_NAME,
                                                           )
        ImageFont.truetype(fqFileName)

        self._gameSettings = GameSettings()     # Be able to read the preferences file
        self._gameState    = GameState()        # Set up the game parameters which uses the above
        self._gameEngine   = GameEngine()       # Then the engine needs to be initialized
        self._intelligence = Intelligence()
        self._computer     = Computer()
        self._galaxy       = Galaxy()           # This essentially finishes initializing most of the game

    def _setupUI(self):
        """
        Create the UI sections including the overlays like long range scan and the warp visual
        The initialization order is fragile
        Message console has to be setup first, because the enterprise mediator is a MissesMediator
        """
        #
        # Message console is public because sub sections use it to send messages
        #
        self.messageConsoleSection = MessageConsoleSection(left=0, bottom=COMMAND_SECTION_HEIGHT, height=CONSOLE_SECTION_HEIGHT, width=SCREEN_WIDTH, accept_keyboard_events=False)
        # Create proxy and inject the console
        self._messageConsoleProxy = MessageConsoleProxy()
        self._messageConsoleProxy.console = self.messageConsoleSection

        self._statusConsole = StatusConsoleSection(left=QUADRANT_GRID_WIDTH, bottom=SCREEN_HEIGHT - QUADRANT_GRID_HEIGHT,
                                                   height=QUADRANT_GRID_HEIGHT + CONSOLE_SECTION_HEIGHT, width=STATUS_VIEW_WIDTH,
                                                   accept_keyboard_events=False)

        self._enterpriseMediator = EnterpriseMediator()

        self._quadrantSection = QuadrantSection(left=0, bottom=SCREEN_HEIGHT - QUADRANT_GRID_HEIGHT,
                                                height=QUADRANT_GRID_HEIGHT, width=QUADRANT_GRID_WIDTH,
                                                accept_keyboard_events=False)

        self._quadrantSection.enterpriseMediator = self._enterpriseMediator

        self._commandInputSection = VatoLocoTextSection(left=0, bottom=0, callback=self._handleCommands, accept_keyboard_events=True)
        #
        # These sections are not enabled by default and disabled externally to here;  So make them public
        #
        self.galaxySection = GalaxySection(left=0, bottom=SCREEN_HEIGHT - CONSOLE_SECTION_HEIGHT, height=QUADRANT_GRID_HEIGHT, width=QUADRANT_GRID_WIDTH)

        self.longRangeSensorScanSection = LongRangeSensorScanSection(left=SCREEN_WIDTH // 2,
                                                                     bottom=(QUADRANT_GRID_HEIGHT // 2) + CONSOLE_SECTION_HEIGHT,
                                                                     width=LongRangeSensorScanSection.BACKGROUND_WIDTH,
                                                                     height=LongRangeSensorScanSection.BACKGROUND_HEIGHT)
        viewWindow: Window = self.window
        viewWidth:  int    = viewWindow.width
        viewHeight: int    = viewWindow.height

        self.warpEffectSection:   WarpEffectSection   = WarpEffectSection(width=viewWidth, height=viewHeight)
        self.deviceStatusSection: DeviceStatusSection = DeviceStatusSection(enabled=False)
        #
        # Make the sections available
        #
        self.section_manager.add_section(self._quadrantSection)
        self.section_manager.add_section(self._statusConsole)
        self.section_manager.add_section(self.messageConsoleSection)
        self.section_manager.add_section(self.galaxySection)
        self.section_manager.add_section(self.longRangeSensorScanSection)
        self.section_manager.add_section(self.warpEffectSection)
        self.section_manager.add_section(self._commandInputSection)
        self.section_manager.add_section(self.deviceStatusSection)

    def _handleCommands(self, commandStr: str):
        try:
            self._commandHandler.doCommand(commandStr=commandStr)
        except InvalidCommandException as ice:
            self.messageConsoleSection.displayMessage(message=str(ice), messageType=ConsoleMessageType.Warning)
        except InvalidCommandValueException as e:
            self.messageConsoleSection.displayMessage(message=str(e), messageType=ConsoleMessageType.Warning)


def main():

    arcadeWindow: Window   = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, resizable=True)
    game:         PyTrekV2 = PyTrekV2()

    arcadeWindow.show_view(game)

    arcadeRun()


if __name__ == '__main__':
    main()
