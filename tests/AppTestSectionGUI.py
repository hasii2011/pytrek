
from arcade import View
from arcade import Window
from arcade import draw_text
from arcade import start_render

from arcade.color import WHITE

from arcade.gui import UIManager

from pytrek.Constants import FIXED_WIDTH_FONT_NAME

from pytrek.guiv2.BaseSection import BaseSection
from pytrek.guiv2.CommandInputSection import CommandInputSection
from tests.ProjectTestBase import ProjectTestBase

WINDOW_WIDTH:  int = 800
WINDOW_HEIGHT: int = 600


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


class MainView(View):

    def __init__(self):
        super().__init__()

        self.inputSection:    CommandInputSection = CommandInputSection(accept_keyboard_events=True)
        self.drawTextSection: DrawTextSection     = DrawTextSection()

        self.section_manager.add_section(self.drawTextSection)
        self.section_manager.add_section(self.inputSection)

    def on_draw(self):
        start_render()


def main():
    ProjectTestBase.setUpLogging()

    window:   Window   = Window(title='Test Section GUI', width=WINDOW_WIDTH, height=WINDOW_HEIGHT, resizable=False)
    mainView: MainView = MainView()

    window.show_view(mainView)
    window.run()


if __name__ == '__main__':
    main()
