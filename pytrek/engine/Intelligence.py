
from logging import Logger
from logging import getLogger
from random import randrange

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS

from pytrek.Singleton import Singleton

from pytrek.objects.Coordinates import Coordinates


QUADRANT_HEIGHT: int = QUADRANT_ROWS
QUADRANT_WIDTH:  int = QUADRANT_COLUMNS


class Intelligence(Singleton):

    def init(self):
        """
        """
        self.logger:  Logger = getLogger(__name__)

    def getRandomSectorCoordinates(self) -> Coordinates:
        """
        Generate a random set of sector coordinates
        """

        x = randrange(QUADRANT_HEIGHT)
        y = randrange(QUADRANT_WIDTH)
        return Coordinates(x, y)
