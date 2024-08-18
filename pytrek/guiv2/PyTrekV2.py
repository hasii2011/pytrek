
from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from PIL import ImageFont

from arcade import View
from arcade import Window

from arcade import run as arcadeRun

from arcade import start_render

from pytrek.CommandHandler import CommandHandler
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

from pytrek.gui.ConsoleMessageType import ConsoleMessageType

from pytrek.guiv2.GalaxySection import GalaxySection
from pytrek.guiv2.LongRangeSensorScanSection import LongRangeSensorScanSection
from pytrek.guiv2.MessageConsoleProxy import MessageConsoleProxy
from pytrek.guiv2.MessageConsoleSection import MessageConsoleSection

from pytrek.guiv2.QuadrantSection import QuadrantSection
from pytrek.guiv2.StatusConsoleSection import StatusConsoleSection
from pytrek.guiv2.VatoLocoTextSection import VatoLocoTextSection
from pytrek.guiv2.WarpEffectSection import WarpEffectSection

SCREEN_TITLE:  str = "PyTrekV2"


class PyTrekV2(View):

    def __init__(self):

        LocateResources.setupSystemLogging()

        self.logger: Logger = getLogger(__name__)
        super().__init__()

        #
        # I am cheating here because I know arcade uses PIL under the covers
        #
        fqFileName: str = LocateResources.getResourcesPath(bareFileName=FIXED_WIDTH_FONT_FILENAME,
                                                           resourcePath=LocateResources.FONT_RESOURCES_PATH,
                                                           packageName=LocateResources.FONT_RESOURCES_PACKAGE_NAME,
                                                           )
        ImageFont.truetype(fqFileName)

        self.messageConsoleSection: MessageConsoleSection = MessageConsoleSection(left=0,
                                                                                  bottom=COMMAND_SECTION_HEIGHT,
                                                                                  height=CONSOLE_SECTION_HEIGHT,
                                                                                  width=SCREEN_WIDTH,
                                                                                  accept_keyboard_events=False
                                                                                  )

        # Create proxy and inject the console
        self._messageConsoleProxy: MessageConsoleProxy = MessageConsoleProxy()
        self._messageConsoleProxy.console = self.messageConsoleSection

        self._statusConsole:   StatusConsoleSection = StatusConsoleSection(left=QUADRANT_GRID_WIDTH, bottom=SCREEN_HEIGHT - QUADRANT_GRID_HEIGHT,
                                                                           height=QUADRANT_GRID_HEIGHT + CONSOLE_SECTION_HEIGHT, width=STATUS_VIEW_WIDTH,
                                                                           accept_keyboard_events=False)

        self._quadrantSection: QuadrantSection      = QuadrantSection(left=0, bottom=SCREEN_HEIGHT - QUADRANT_GRID_HEIGHT,
                                                                      height=QUADRANT_GRID_HEIGHT, width=QUADRANT_GRID_WIDTH,
                                                                      accept_keyboard_events=False)

        self._commandInputSection: VatoLocoTextSection = VatoLocoTextSection(left=0, bottom=0, callback=self._handleCommands, accept_keyboard_events=True)

        # These sections are not enabled by default and disabled externally to here;  So make them public
        self.galaxySection: GalaxySection = GalaxySection(left=0,
                                                          bottom=SCREEN_HEIGHT - CONSOLE_SECTION_HEIGHT,
                                                          height=QUADRANT_GRID_HEIGHT,
                                                          width=QUADRANT_GRID_WIDTH)

        self.longRangeSensorScanSection: LongRangeSensorScanSection = LongRangeSensorScanSection(left=SCREEN_WIDTH // 2,
                                                                                                 bottom=(QUADRANT_GRID_HEIGHT // 2) + CONSOLE_SECTION_HEIGHT,
                                                                                                 width=LongRangeSensorScanSection.BACKGROUND_WIDTH,
                                                                                                 height=LongRangeSensorScanSection.BACKGROUND_HEIGHT)

        viewWindow: Window = self.window
        viewWidth:  int = viewWindow.width
        viewHeight: int = viewWindow.height
        self.warpEffectSection: WarpEffectSection = WarpEffectSection(width=viewWidth, height=viewHeight)

        # add the sections
        self.section_manager.add_section(self._quadrantSection)
        self.section_manager.add_section(self._statusConsole)
        self.section_manager.add_section(self.messageConsoleSection)
        self.section_manager.add_section(self.galaxySection)
        self.section_manager.add_section(self.longRangeSensorScanSection)
        self.section_manager.add_section(self.warpEffectSection)
        self.section_manager.add_section(self._commandInputSection)

        #
        # TODO: fix this later
        # The quadrant section initialized the various singletons in the correct order
        #
        self._commandHandler: CommandHandler = CommandHandler(view=self)

    def on_draw(self):
        start_render()

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
