
from typing import List

from logging import Logger
from logging import getLogger
from typing import NewType

from arcade import Sprite
from arcade import SpriteList
from arcade import SpriteSolidColor
from arcade import color

from Constants import SCREEN_HEIGHT

QUADRANT_GRID_WIDTH:  int = 640
QUADRANT_GRID_HEIGHT: int = 640

QUADRANT_PIXEL_HEIGHT: int = 64
QUADRANT_PIXEL_WIDTH:  int = 64
QUADRANT_Y_ADJUSTMENT: int = SCREEN_HEIGHT - QUADRANT_GRID_HEIGHT   # Adjustment from bottom

QUADRANT_ROWS:    int = 10
QUADRANT_COLUMNS: int = 10
MARGIN: int = 1

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

        # Create a list of solid-color sprites to represent each grid location
        for row in range(QUADRANT_ROWS):
            self._gridSprites.append([])
            for column in range(QUADRANT_COLUMNS):
                x = column * (QUADRANT_PIXEL_WIDTH + MARGIN) + (QUADRANT_PIXEL_WIDTH / 2 + MARGIN)
                y = row * (QUADRANT_PIXEL_HEIGHT + MARGIN) + (QUADRANT_PIXEL_HEIGHT / 2 + MARGIN)
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
