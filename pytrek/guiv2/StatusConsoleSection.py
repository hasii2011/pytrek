from enum import Enum
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger
from typing import Union

from arcade import Section
from arcade import draw_text
from arcade.color import BLUE
from arcade.color import GREEN
from arcade.color import RED

from arcade.color import WHITE
from arcade.color import YELLOW

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_NAME
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.GameState import GameState
from pytrek.engine.ShipCondition import ShipCondition

from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.gui.LogMessageConsole import LogMessageConsole
from pytrek.model.Coordinates import Coordinates

from pytrek.settings.GameSettings import GameSettings


SECTION_LABEL_FONT_SIZE: int = 16
STATUS_LABEL_FONT_SIZE: int = 11
STATUS_TEXT_COLOR = WHITE           # has no type

TITLE_MARGIN_X: int = 20
TITLE_MARGIN_Y: int = 10
TITLE_FONT_OFFSET_Y: int = 24

START_STATUS_OFFSET:   int = -30  # Because arcade 0,0 is at bottom left
INLINE_STATUS_OFFSET:  int = -20
STATUS_VALUE_X_OFFSET: int = 110

PropertyName  = NewType('PropertyName', str)
PropertyNames = NewType('PropertyNames', List[PropertyName])


class StatusConsoleSection(Section):

    statusLabels: List[str] = [
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

    def __init__(self, left: int, bottom: int, width: int, height: int, **kwargs):

        self.logger: Logger = getLogger(__name__)
        super().__init__(left, bottom, width, height, **kwargs)

        self._gameSettings: GameSettings = GameSettings()
        self._gameState:    GameState    = GameState()
        self._eventEngine:  EventEngine  = EventEngine(LogMessageConsole())

        self._statusProperties: PropertyNames = PropertyNames([])

        self._statusProperties.append(PropertyName('shipCondition'))
        self._statusProperties.append(PropertyName('starDate'))
        self._statusProperties.append(PropertyName('currentQuadrantCoordinates'))
        self._statusProperties.append(PropertyName('currentSectorCoordinates'))
        self._statusProperties.append(PropertyName('energy'))
        self._statusProperties.append(PropertyName('shieldEnergy'))
        self._statusProperties.append(PropertyName('remainingGameTime'))
        self._statusProperties.append(PropertyName('remainingKlingons'))
        self._statusProperties.append(PropertyName('remainingCommanders'))
        self._statusProperties.append(PropertyName('torpedoCount'))

    def on_draw(self):
        """
        Remember arcade's 0,0 origin is lower left corner
        """

        statusConsoleLabelX = self.left + TITLE_MARGIN_X
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
        for label in StatusConsoleSection.statusLabels:
            draw_text(label, labelX, runningY, color=STATUS_TEXT_COLOR, font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)
            runningY = runningY + INLINE_STATUS_OFFSET

    def drawStatusValues(self, statusX: int, runningY: int):

        statusProperties: PropertyNames = self._statusProperties

        for propertyName in statusProperties:

            propertyValue: Union[Enum, float, int, str] = getattr(self._gameState, propertyName)
            propertyStr: str = ''

            baseTextColor = STATUS_TEXT_COLOR
            if isinstance(propertyValue, ShipCondition):
                propertyStr = propertyValue.__str__()
                baseTextColor = self._getStatusColor(shipCondition=propertyValue)
            elif isinstance(propertyValue, float):
                propertyStr = f'{propertyValue:.0f}'
            elif isinstance(propertyValue, int):
                propertyStr = str(propertyValue)
            elif isinstance(propertyValue, Coordinates):
                propertyStr = self._formatCoordinates(coordinates=propertyValue)

            draw_text(propertyStr, statusX, runningY, color=baseTextColor,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            runningY = runningY + INLINE_STATUS_OFFSET

        self._showInternalValues(runningY, statusX)

    def _getStatusColor(self, shipCondition: ShipCondition):

        if shipCondition == ShipCondition.Green:
            return GREEN
        elif shipCondition == ShipCondition.Yellow:
            return YELLOW
        elif shipCondition == ShipCondition.Red:
            return RED
        elif shipCondition == ShipCondition.Docked:
            return BLUE
        else:
            return WHITE

    def _formatCoordinates(self, coordinates: Coordinates) -> str:
        """
        Nicely formats the input coordinates in the form:   (x,y)
        Args:
            coordinates: Coordinates to format

        Returns:  The formatted coordinates
        """
        return f'({coordinates.x},{coordinates.y})'

    def _showInternalValues(self, runningY: int, statusX: int):

        labelX:      int = QUADRANT_GRID_WIDTH + TITLE_MARGIN_X
        compressedX: int = statusX - 16
        currentY:    int = runningY

        currentY = currentY + INLINE_STATUS_OFFSET

        if self._gameSettings.consoleShowInternals is True:

            draw_text('OpTime:', labelX, currentY, color=RED,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            opTimeStr: str = f'{self._gameState.opTime:.2f}'
            draw_text(opTimeStr, compressedX, currentY, color=RED,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)
            #
            currentY = currentY + INLINE_STATUS_OFFSET
            draw_text('T Beam:', labelX, currentY, color=RED,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            evtStr: str = self.__getTimeString(FutureEventType.TRACTOR_BEAM)
            draw_text(evtStr, compressedX, currentY, color=RED,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            currentY = currentY + INLINE_STATUS_OFFSET
            draw_text('SNova:', labelX, currentY, color=RED,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            evtStr = self.__getTimeString(FutureEventType.SUPER_NOVA)
            draw_text(evtStr, compressedX, currentY, color=RED,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            currentY = currentY + INLINE_STATUS_OFFSET
            draw_text('CAttack:', labelX, currentY, color=RED,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            evtStr = self.__getTimeString(FutureEventType.COMMANDER_ATTACKS_BASE)
            draw_text(evtStr, compressedX, currentY, color=RED,
                      font_size=STATUS_LABEL_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

    def __getTimeString(self, eventType: FutureEventType):

        fEvent: FutureEvent = self._eventEngine.getEvent(eventType)
        evtStr: str = f'{fEvent.starDate:.2f}'

        return evtStr
