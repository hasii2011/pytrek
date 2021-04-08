
from logging import Logger
from logging import getLogger
from random import randrange

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS

from pytrek.Singleton import Singleton

from pytrek.objects.Coordinates import Coordinates


class Intelligence(Singleton):

    def init(self):
        """
        """
        self.logger:  Logger = getLogger(__name__)

    def generateSectorCoordinates(self) -> Coordinates:
        """
        Generate a random set of sector coordinates
        """

        x = randrange(QUADRANT_COLUMNS)
        y = randrange(QUADRANT_ROWS)

        return Coordinates(x=x, y=y)
