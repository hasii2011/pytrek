from arcade import start_render
from arcade.color import GREEN
from arcade.color import WHITE

from arcade import draw_text

from pytrek.Constants import FIXED_WIDTH_FONT_NAME

from pytrek.guiv2.BaseSection import BaseSection


class DrawTextSection(BaseSection):
    def __init__(self, **kwargs):

        window = self.window

        w: int = window.width  // 6
        h: int = window.height // 10

        super().__init__(left=30, bottom=530, width=w, height=h, **kwargs)

    def on_draw(self):
        """
        Remember arcade's 0,0 origin is lower left corner
        """
        start_render()
        x: int = self.left + 5
        y: int = self.bottom + 10
        self.drawDebug(color=GREEN)

        draw_text('Drawn Text', x, y, color=WHITE, font_size=18, font_name=FIXED_WIDTH_FONT_NAME)
