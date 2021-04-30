from logging import Logger
from logging import getLogger
from typing import cast

from arcade import View
from arcade import color
from arcade import draw_text

from pytrek.Constants import QUADRANT_PIXEL_HEIGHT
from pytrek.Constants import QUADRANT_PIXEL_WIDTH
from pytrek.Singleton import Singleton
from pytrek.engine.Computer import Computer
from pytrek.engine.Direction import Direction

from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.LRScanCoordinates import LRScanCoordinates

from pytrek.model.Coordinates import Coordinates
from pytrek.model.DataTypes import LRScanCoordinatesList
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

LR_SCAN_FONT_SIZE: int = 14


class LongRangeSensorScanMediator(Singleton):

    def init(self, *args, **kwds):
        """
        Accepts the following keyword arguments:
        * view The arcade view for the long range scan
        * graphicCenterX  The background center X position
        * graphicCenterY  The background center Y position
        Args:
            *args:
            **kwds:

        """

        self.logger: Logger = getLogger(__name__)

        self._intelligence: Intelligence = Intelligence()
        self._computer:     Computer     = Computer()
        self._galaxy:       Galaxy       = Galaxy()

        self.view: View = cast(View, None)
        self.graphicCenterX: float = 0
        self.graphicCenterY: float = 0

        self._setKeywordParameters(**kwds)

        self._windowWidth:  int = self.view.window.width
        self._windowHeight: int = self.view.window.height

    def update(self, centerCoordinates: Coordinates):

        coordinatesList: LRScanCoordinatesList = self._intelligence.generateAdjacentCoordinates(centerCoordinates=centerCoordinates)

        graphicCenterX: float = self.graphicCenterX
        graphicCenterY: float = self.graphicCenterY

        titleX: float = graphicCenterX - (QUADRANT_PIXEL_WIDTH * 2) - (QUADRANT_PIXEL_WIDTH / 2)
        titleY: float = graphicCenterY + (QUADRANT_PIXEL_HEIGHT * 2) + (QUADRANT_PIXEL_HEIGHT / 2)
        title:  str = f'Long Range Scan quadrant ({centerCoordinates.x},{centerCoordinates.y})'
        draw_text(title,  titleX, titleY, color.WHITE, 18)

        draw_text("E", graphicCenterX - 4, graphicCenterY - 8, color.YELLOW, LR_SCAN_FONT_SIZE)    # Adjust for font size

        for scanCoordinates in coordinatesList:
            self.logger.debug(f'{scanCoordinates=}')
            self._drawQuadrantContents(scanCoordinates=scanCoordinates, centerX=graphicCenterX, centerY=graphicCenterY)

    def _setKeywordParameters(self, **kwds):
        """
        Scans the keyword argument input list and attempts to set the defined instance properties;  "Declare"
        instance variables you wish to accept prior to calling this method
        Args:
            **kwds:
        """
        for name, value in kwds.items():
            if not hasattr(self, name):
                raise TypeError(f"Unexpected keyword argument `{name}`")
            setattr(self, name, value)

    def _drawQuadrantContents(self, scanCoordinates: LRScanCoordinates, centerX: float, centerY: float):

        drawX: float = centerX
        drawY: float = centerY

        if scanCoordinates.direction == Direction.North:
            drawX = drawX - LR_SCAN_FONT_SIZE
            drawY = drawY + QUADRANT_PIXEL_HEIGHT - LR_SCAN_FONT_SIZE
        elif scanCoordinates.direction == Direction.South:
            drawX = drawX - LR_SCAN_FONT_SIZE
            drawY = drawY - QUADRANT_PIXEL_HEIGHT - LR_SCAN_FONT_SIZE
        elif scanCoordinates.direction == Direction.West:
            drawX = drawX - QUADRANT_PIXEL_WIDTH - LR_SCAN_FONT_SIZE
            drawY = drawY - LR_SCAN_FONT_SIZE + 4
        elif scanCoordinates.direction == Direction.East:
            drawX = drawX + QUADRANT_PIXEL_WIDTH - LR_SCAN_FONT_SIZE
            drawY = drawY - LR_SCAN_FONT_SIZE + 4
        elif scanCoordinates.direction == Direction.NorthEast:
            drawX = drawX + QUADRANT_PIXEL_WIDTH - LR_SCAN_FONT_SIZE
            drawY = drawY + QUADRANT_PIXEL_HEIGHT - LR_SCAN_FONT_SIZE
        elif scanCoordinates.direction == Direction.NorthWest:
            drawX = drawX - QUADRANT_PIXEL_WIDTH - LR_SCAN_FONT_SIZE
            drawY = drawY + QUADRANT_PIXEL_HEIGHT - LR_SCAN_FONT_SIZE
        elif scanCoordinates.direction == Direction.SouthWest:
            drawX = drawX - QUADRANT_PIXEL_WIDTH - LR_SCAN_FONT_SIZE
            drawY = drawY - QUADRANT_PIXEL_HEIGHT - LR_SCAN_FONT_SIZE
        elif scanCoordinates.direction == Direction.SouthEast:
            drawX = drawX + QUADRANT_PIXEL_WIDTH - LR_SCAN_FONT_SIZE
            drawY = drawY - QUADRANT_PIXEL_HEIGHT - LR_SCAN_FONT_SIZE

        quadrant: Quadrant = self._galaxy.getQuadrant(quadrantCoordinates=scanCoordinates.coordinates)

        quadrant.scanned = True

        contents: str = self._computer.createValueString(klingonCount=quadrant.klingonCount,
                                                         commanderCount=quadrant.commanderCount,
                                                         hasStarBase=quadrant.hasStarBase)
        draw_text(contents, drawX, drawY, color.WHITE, LR_SCAN_FONT_SIZE)
