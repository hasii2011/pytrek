
from arcade import View
from arcade import Window

from arcade.color import BLACK

from arcade import run as arcadeRun

from arcade import schedule
from arcade import unschedule

from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH

from pytrek.guiv2.WarpEffectSection import WarpEffectSection

from tests.AppTestWarpDialogSection import DrawTextSection

from tests.ProjectTestBase import ProjectTestBase

SCREEN_TITLE: str = 'Test Warp Effect Section'


class TestView(View):
    """
    The test view
    """

    def __init__(self):
        super().__init__()

        self._drawTextSection:   DrawTextSection   = DrawTextSection(enabled=True)
        self._warpEffectSection: WarpEffectSection = WarpEffectSection(width=self.window.width, height=self.window.height)

        self._warpEffectSection.setup()
        self.section_manager.add_section(self._drawTextSection)
        self.section_manager.add_section(self._warpEffectSection)

        schedule(function_pointer=self.checkEffectComplete, interval=1.0)  # type:ignore

        self._warpEffectSection.enabled = True

    def on_draw(self):
        pass


def main():

    ProjectTestBase.setUpLogging()

    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    arcadeWindow.background_color = BLACK
    arcadeWindow.clear()

    testView: TestView = TestView()
    arcadeWindow.show_view(testView)

    arcadeRun()


if __name__ == "__main__":
    main()
