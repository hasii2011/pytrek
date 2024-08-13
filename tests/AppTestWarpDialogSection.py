
from arcade import View
from arcade import Window
from arcade import draw_text

from arcade import start_render
from arcade import exit as arcadeExit
from arcade.color import WHITE

from pytrek.Constants import FIXED_WIDTH_FONT_NAME
from pytrek.guiv2.BaseSection import BaseSection
from pytrek.guiv2.WarpDialogSection import DialogAnswer
from pytrek.guiv2.WarpDialogSection import WarpDialogSection
from pytrek.guiv2.WarpDialogSection import WarpTravelAnswer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Test Warp Dialog"


def completeCallback(warpTravelAnswer: WarpTravelAnswer):

    if warpTravelAnswer.dialogAnswer == DialogAnswer.Cancelled:
        arcadeExit()
    else:
        print(f'{warpTravelAnswer=}')


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
    """ The game itself """

    def __init__(self):
        super().__init__()

        x:  int = self.window.width // 3
        y: int = (self.window.height // 3)
        self._warpDialogSection: WarpDialogSection = WarpDialogSection(left=x, bottom=y,
                                                                       width=400, height=200,
                                                                       completeCallback=completeCallback,
                                                                       accept_keyboard_events=True
                                                                       )

        self._drawTextSection: DrawTextSection     = DrawTextSection(accept_keyboard_events=False)

        # self.section_manager.add_section(self._drawTextSection)
        self.section_manager.add_section(self._warpDialogSection)

    def on_draw(self):
        start_render()


def main():
    window:   Window   = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    testView: TestView = TestView()

    window.show_view(testView)
    window.run()


if __name__ == '__main__':
    main()
