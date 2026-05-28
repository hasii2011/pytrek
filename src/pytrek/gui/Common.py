
from typing import List

from dataclasses import dataclass

from arcade import Rect
from arcade import Texture

from arcade import draw_rect_filled
from arcade import draw_texture_rect

from codeallybasic.SecureConversions import SecureConversions

from pytrek.Constants import COMMAND_SECTION_HEIGHT
from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import SCREEN_WIDTH


@dataclass
class PyTrekColor:
    r: int = 0
    g: int = 0
    b: int = 0
    alpha: int = 0

    @classmethod
    def deSerialize(cls, value: str) -> 'PyTrekColor':
        """
        The input string is in the format created by __str__()
        
        Args:
            value: 

        Returns:  A PyTrekColorValue

        """
        splitValue: List[str] = value.split(sep=',')

        r:     int = SecureConversions.secureInteger(splitValue[0])
        g:     int = SecureConversions.secureInteger(splitValue[1])
        b:     int = SecureConversions.secureInteger(splitValue[2])
        alpha: int = SecureConversions.secureInteger(splitValue[3])

        return PyTrekColor(r=r, g=g, b=b, alpha=alpha,)

    def __str__(self) -> str:
        return f'{self.r},{self.g},{self.b},{self.alpha}'

    def __repr__(self):
        return f'PyTrekColor: {self.__str__()}'


def drawQuadrantGrid(background: Texture):
    """
    Draw the background texture
    Args:
        background:
    """

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

def dimBackgroundForView(windowWidth: int, windowHeight: int):
    """

    Args:
        windowWidth:
        windowHeight:

    """
    from pytrek.settings.GameSettings import GameSettings

    viewDimRGBA: PyTrekColor = GameSettings().viewDimRGBA

    draw_rect_filled(
        rect=Rect.from_kwargs(
            x=windowWidth / 2,
            y=windowHeight / 2,
            width=windowWidth,
            height=windowHeight
        ),
        color=(viewDimRGBA.r, viewDimRGBA.g, viewDimRGBA.b, viewDimRGBA.alpha)    # RGBA color: (red, green, blue, alpha)
    )
