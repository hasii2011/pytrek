from logging import Logger
from logging import getLogger

from arcade import color
from arcade import draw_text

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Singleton import Singleton
from pytrek.engine.Intelligence import Intelligence
from pytrek.model.Coordinates import Coordinates
from pytrek.model.DataTypes import CoordinatesList
from pytrek.model.Quadrant import Quadrant


class LongRangeSensorScanMediator(Singleton):

    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        self._intelligence: Intelligence = Intelligence()

    def update(self, centerCoordinates: Coordinates):

        coordinatesList: CoordinatesList = self._intelligence.generateAdjacentCoordinates(centerCoordinates=centerCoordinates)

        start_x = 50
        start_y = (QUADRANT_GRID_HEIGHT + CONSOLE_HEIGHT) - 24
        draw_text("Long Range Sensor Scan Coming Soon", start_x, start_y, color.WHITE, 14)
