
from logging import Logger
from logging import getLogger

from arcade import Section
from arcade import draw_lrtb_rectangle_outline

from arcade.color import GREEN


class BaseSection(Section):

    def __init__(self, left: int, bottom: int, width: int, height: int, **kwargs):

        super().__init__(left, bottom, width, height, **kwargs)

        self.logger: Logger = getLogger(__name__)

    def on_draw(self):
        draw_lrtb_rectangle_outline(left=self.left+2, right=self.right-2, top=self.top, bottom=self.bottom, color=GREEN, border_width=1)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        super().on_key_release(symbol, modifiers)
