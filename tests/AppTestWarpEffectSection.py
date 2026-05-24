
from arcade import View
from arcade import Window

from arcade.color import BLACK

from arcade import schedule

from arcade import SectionManager

from arcade import run as arcadeRun

from src.pytrek.Constants import SCREEN_HEIGHT
from src.pytrek.Constants import SCREEN_WIDTH

from src.pytrek.gui.WarpEffectSection import WarpEffectSection
from tests.DrawTextSection import DrawTextSection

from tests.ProjectTestBase import ProjectTestBase

SCREEN_TITLE: str = 'Test Warp Effect Section'


class TestView(View):
    """
    The test view
    """

    def __init__(self):
        super().__init__()

        self.sectionManager: SectionManager = SectionManager(self)

        self._drawTextSection:   DrawTextSection   = DrawTextSection(enabled=True)
        self._warpEffectSection: WarpEffectSection = WarpEffectSection(width=self.window.width, height=self.window.height)

        self._warpEffectSection.setup()
        self.sectionManager.add_section(self._drawTextSection)
        self.sectionManager.add_section(self._warpEffectSection)

        schedule(function_pointer=self.checkEffectComplete, interval=1.0)

        self._warpEffectSection.enabled = True

    def on_draw(self):
        self.clear()

    def on_show_view(self):
        self.sectionManager.enable()
        from arcade import schedule
        schedule(self.checkEffectComplete, 1.0)

    def on_hide_view(self):
        self.sectionManager.disable()

    def checkEffectComplete(self, delta_time: float):
        """
        Periodically check if the warp effect is finished
        """
        if self._warpEffectSection.isEffectComplete():
            from arcade import unschedule
            print("Warp test effect complete.")
            unschedule(self.checkEffectComplete)
            self._warpEffectSection.enabled = False


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
