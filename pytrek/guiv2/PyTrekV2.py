
from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from PIL import ImageFont

from arcade import View
from arcade import Window

from arcade import run as arcadeRun

from arcade import start_render

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_FILENAME
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.Constants import STATUS_VIEW_WIDTH

from pytrek.LocateResources import LocateResources
from pytrek.guiv2.GalaxySection import GalaxySection
from pytrek.guiv2.LongRangeSensorScanSection import LongRangeSensorScanSection
from pytrek.guiv2.MessageConsoleProxy import MessageConsoleProxy
from pytrek.guiv2.MessageConsoleSection import MessageConsoleSection

from pytrek.guiv2.QuadrantSection import QuadrantSection
from pytrek.guiv2.StatusConsoleSection import StatusConsoleSection


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

        left:   int = QUADRANT_GRID_WIDTH
        bottom: int = QUADRANT_GRID_HEIGHT
        height: int = QUADRANT_GRID_HEIGHT + CONSOLE_HEIGHT
        width:  int = STATUS_VIEW_WIDTH

        self._messageConsoleSection: MessageConsoleSection = MessageConsoleSection(left=0, bottom=0,
                                                                                   height=CONSOLE_HEIGHT, width=SCREEN_WIDTH,
                                                                                   accept_keyboard_events=False
                                                                                   )

        # Create proxy and inject the console
        self._messageConsoleProxy: MessageConsoleProxy = MessageConsoleProxy()
        self._messageConsoleProxy.console = self._messageConsoleSection

        self._statusConsole:   StatusConsoleSection = StatusConsoleSection(left=left, bottom=bottom, height=height, width=width,
                                                                           accept_keyboard_events=False)

        self._quadrantSection: QuadrantSection      = QuadrantSection(left=0, bottom=CONSOLE_HEIGHT, height=QUADRANT_GRID_HEIGHT, width=QUADRANT_GRID_WIDTH,
                                                                      accept_keyboard_events=True)

        # These sections are not enabled by default and disabled externally to here;  So make them public
        self.galaxySection: GalaxySection = GalaxySection(left=0,
                                                          bottom=SCREEN_HEIGHT - CONSOLE_HEIGHT,
                                                          height=QUADRANT_GRID_HEIGHT,
                                                          width=QUADRANT_GRID_WIDTH)

        self.longRangeSensorScanSection: LongRangeSensorScanSection = LongRangeSensorScanSection(left=SCREEN_WIDTH // 2,
                                                                                                 bottom=(QUADRANT_GRID_HEIGHT // 2) + CONSOLE_HEIGHT,
                                                                                                 width=LongRangeSensorScanSection.BACKGROUND_WIDTH,
                                                                                                 height=LongRangeSensorScanSection.BACKGROUND_HEIGHT)
        # add the sections
        self.section_manager.add_section(self._quadrantSection)
        self.section_manager.add_section(self._statusConsole)
        self.section_manager.add_section(self._messageConsoleSection)
        self.section_manager.add_section(self.galaxySection)
        self.section_manager.add_section(self.longRangeSensorScanSection)

    def on_draw(self):
        start_render()


def main():
    arcadeWindow: Window   = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    game:         PyTrekV2 = PyTrekV2()

    arcadeWindow.show_view(game)

    arcadeRun()


if __name__ == '__main__':
    main()
