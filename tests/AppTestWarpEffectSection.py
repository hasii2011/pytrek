
from arcade import View
from arcade import Window
from arcade import draw_text
from arcade import schedule
from arcade import unschedule

from arcade.color import BLACK


from arcade import run as arcadeRun
from arcade.color import WHITE

from pytrek.Constants import FIXED_WIDTH_FONT_NAME
from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.guiv2.BaseSection import BaseSection

from pytrek.guiv2.WarpEffectSection import WarpEffectSection

from tests.ProjectTestBase import ProjectTestBase

SCREEN_TITLE: str = 'Test Warp Effect Section'


class DrawTextSection(BaseSection):
    def __init__(self, **kwargs):

        window = self.window

        w: int = window.width  // 4
        h: int = window.height // 10

        super().__init__(left=30, bottom=530, width=w, height=h, **kwargs)

    def on_draw(self):
        """
        Remember arcade's 0,0 origin is lower left corner
        """
        x: int = self.left + 5
        y: int = self.bottom + 10
        super().on_draw()
        draw_text('Drawn Text', x, y, color=WHITE, font_size=18, font_name=FIXED_WIDTH_FONT_NAME)


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

    def checkEffectComplete(self, deltaTime: float):

        effectComplete: bool = self._warpEffectSection.isEffectComplete()
        if effectComplete is True:
            print('Warp effect is done')
            unschedule(self.checkEffectComplete)
            self._warpEffectSection.enabled = False

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
