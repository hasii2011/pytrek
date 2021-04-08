
from typing import List

from logging import Logger
from logging import getLogger
from typing import NewType

from arcade import Sprite
from arcade import SpriteList
from arcade import SpriteSolidColor
from arcade import color

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_MARGIN
from pytrek.Constants import QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import QUADRANT_PIXEL_WIDTH
from pytrek.Constants import QUADRANT_ROWS
from pytrek.Constants import QUADRANT_Y_ADJUSTMENT

SpriteRow  = NewType('SpriteRow', List[Sprite])
SpriteGrid = NewType('SpriteGrid', List[SpriteRow])


class QuadrantBackground:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        # One dimensional list of all sprites in the two-dimensional sprite list
        self._gridSpriteList: SpriteList = SpriteList()

        # This is a two-dimensional grid of sprites that mirrors the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in gridSpriteList, just in a 2D manner.
        self._gridSprites: SpriteGrid = SpriteGrid([])

        # Create a list of solid-color sprites to represent each sector location
        for row in range(QUADRANT_ROWS):
            self._gridSprites.append([])
            for column in range(QUADRANT_COLUMNS):
                x = column * (QUADRANT_PIXEL_WIDTH + QUADRANT_MARGIN) + (QUADRANT_PIXEL_WIDTH / 2 + QUADRANT_MARGIN)
                y = row * (QUADRANT_PIXEL_HEIGHT + QUADRANT_MARGIN) + (QUADRANT_PIXEL_HEIGHT / 2 + QUADRANT_MARGIN)
                y += QUADRANT_Y_ADJUSTMENT
                sprite: SpriteSolidColor = SpriteSolidColor(QUADRANT_PIXEL_WIDTH, QUADRANT_PIXEL_HEIGHT, color.BLACK)
                sprite.center_x = x
                sprite.center_y = y

                self._gridSpriteList.append(sprite)
                self._gridSprites[row].append(sprite)
        self.logger.warning(f'{len(self._gridSpriteList)=}')

    @property
    def gridSpriteList(self) -> SpriteList:
        return self._gridSpriteList

    def gridSprites(self) -> SpriteGrid:
        return self._gridSprites
