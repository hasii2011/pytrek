#
# yeah, I know when you have "common" or "util" or "utility" modules
# you have a problem in your design;
# I will take on a little bit of technical debt while
# I refactor my unit tests to use sections
#
from arcade import Rect
from arcade import Texture

from arcade import draw_texture_rect

from src.pytrek.Constants import COMMAND_SECTION_HEIGHT
from src.pytrek.Constants import CONSOLE_SECTION_HEIGHT
from src.pytrek.Constants import QUADRANT_GRID_HEIGHT
from src.pytrek.Constants import SCREEN_WIDTH


def drawQuadrantGrid(background: Texture):
    """
    Draw the background texture
    Args:
        background:
    """

    # draw_lrwh_rectangle_textured(bottom_left_x=1,
    #                              bottom_left_y=CONSOLE_SECTION_HEIGHT + COMMAND_SECTION_HEIGHT,
    #                              width=SCREEN_WIDTH,
    #                              height=QUADRANT_GRID_HEIGHT,
    #                              texture=background
    #                              )

    rect: Rect = Rect.from_kwargs(
        left=1,
        bottom=CONSOLE_SECTION_HEIGHT + COMMAND_SECTION_HEIGHT,
        width=SCREEN_WIDTH,
        height=QUADRANT_GRID_HEIGHT
    )

    draw_texture_rect(
        texture=background,
        rect=rect
    )
