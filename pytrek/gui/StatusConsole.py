
from typing import List
from typing import NewType
from typing import Union

from logging import Logger
from logging import getLogger

from enum import Enum

from arcade import View
from arcade import color
from arcade import draw_text

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_NAME
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import QUADRANT_GRID_WIDTH

from pytrek.GameState import GameState

from pytrek.engine.ShipCondition import ShipCondition

from pytrek.model.Coordinates import Coordinates

SECTION_LABEL_FONT_SIZE: int = 16
STATUS_LABEL_FONT_SIZE: int = 11
STATUS_TEXT_COLOR: color = color.WHITE

TITLE_MARGIN_X: int = 10
TITLE_MARGIN_Y: int = 10
TITLE_FONT_OFFSET_Y: int = 24

START_STATUS_OFFSET:   int = -30  # Because arcade 0,0 is at bottom left
INLINE_STATUS_OFFSET:  int = -20
STATUS_VALUE_X_OFFSET: int = 90

PropertyName  = NewType('PropertyName', str)
PropertyNames = NewType('PropertyNames', List[PropertyName])


class StatusConsole:
    """
    This class is not really a view;  It is essentially a chunk of code
    that knows here to draw on the game view.  The game view
    has a reserved portion of the UI set aside for it
    """

    statusLabel: List[str] = [
        'Condition:',
        'StarDate: ',
        'Quadrant:',
        'Sector:',
        'Energy:',
        'Shields:',
        'Game Time:',
        'Klingons:',
        'Commanders:',
        'Torpedoes:'
    ]

    def __init__(self, gameView: View):

        self.logger: Logger = getLogger(__name__)

        self._gameView: View = gameView

        self._gameState: GameState = GameState()

        self._statusProperties: PropertyNames = PropertyNames([])

        self._statusProperties.append('shipCondition')
        self._statusProperties.append('starDate')
        self._statusProperties.append('currentQuadrantCoordinates')
        self._statusProperties.append('currentSectorCoordinates')
        self._statusProperties.append('energy')
        self._statusProperties.append('shieldEnergy')
        self._statusProperties.append('remainingGameTime')
        self._statusProperties.append('remainingKlingons')
        self._statusProperties.append('remainingCommanders')
        self._statusProperties.append('torpedoCount')

    def draw(self):

        statusConsoleLabelX = QUADRANT_GRID_WIDTH + TITLE_MARGIN_X
        statusConsoleLabelY = (QUADRANT_GRID_HEIGHT + CONSOLE_HEIGHT) - TITLE_FONT_OFFSET_Y - TITLE_MARGIN_Y
        draw_text("Status Console", statusConsoleLabelX, statusConsoleLabelY, color=STATUS_TEXT_COLOR,
                  font_size=SECTION_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

        labelX:   int = statusConsoleLabelX
        runningY: int = statusConsoleLabelY + START_STATUS_OFFSET

        self.drawStatusLabels(labelX, runningY)

        runningY = statusConsoleLabelY + START_STATUS_OFFSET    # reset it
        statusX: int = labelX + STATUS_VALUE_X_OFFSET

        self.drawStatusValues(statusX=statusX, runningY=runningY)

    def drawStatusLabels(self, labelX: int, runningY: int):
        """

        Args:
            labelX:   The fixed X location for all the labels
            runningY: The y position for the labels that we update as we move down the label list
        """
        for label in StatusConsole.statusLabel:
            draw_text(label, labelX, runningY, color=STATUS_TEXT_COLOR,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)
            runningY = runningY + INLINE_STATUS_OFFSET

    def drawStatusValues(self, statusX: int, runningY: int):

        statusProperties: PropertyNames = self._statusProperties

        for propertyName in statusProperties:

            propertyValue: Union[Enum, float, int, str] = getattr(self._gameState, propertyName)
            propertyStr: str = ''

            baseTextColor: color = STATUS_TEXT_COLOR
            if isinstance(propertyValue, ShipCondition):
                propertyStr = propertyValue.__str__()
                baseTextColor = self._getStatusColor(shipCondition=propertyValue)
            elif isinstance(propertyValue, float):
                propertyStr = f'{propertyValue:.2f}'
            elif isinstance(propertyValue, int):
                propertyStr = str(propertyValue)
            elif isinstance(propertyValue, Coordinates):
                propertyStr = self._formatCoordinates(coordinates=propertyValue)

            draw_text(propertyStr, statusX, runningY, color=baseTextColor,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            runningY = runningY + INLINE_STATUS_OFFSET

    def _getStatusColor(self, shipCondition: ShipCondition) -> color:

        if shipCondition == ShipCondition.Green:
            return color.GREEN
        elif shipCondition == ShipCondition.Yellow:
            return color.YELLOW
        elif shipCondition == ShipCondition.Red:
            return color.RED
        elif shipCondition == ShipCondition.Docked:
            return color.BLUE
        else:
            return color.WHITE

    def _formatCoordinates(self, coordinates: Coordinates) -> str:
        """
        Nicely formats the input coordinates in the form:   (x,y)
        Args:
            coordinates: Coordinates to format

        Returns:  The formatted coordinates
        """
        return f'({coordinates.x},{coordinates.y})'