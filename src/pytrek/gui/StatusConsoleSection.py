
from typing import Union
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from enum import Enum

from arcade import Text
from arcade import draw_text
from arcade.color import BLUE
from arcade.color import GREEN
from arcade.color import RED

from arcade.color import WHITE
from arcade.color import YELLOW

from pytrek.Constants import COMMAND_SECTION_HEIGHT
from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_NAME
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.GameState import GameState

from pytrek.engine.ShipCondition import ShipCondition

from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.gui.BaseSection import BaseSection
from pytrek.gui.MessageConsoleProxy import MessageConsoleProxy

from pytrek.model.Coordinates import Coordinates

from pytrek.settings.GameSettings import GameSettings


SECTION_LABEL_FONT_SIZE: int = 16
STATUS_LABEL_FONT_SIZE: int = 11
STATUS_TEXT_COLOR = WHITE           # has no type

TITLE_MARGIN_X: int = 10
TITLE_MARGIN_Y: int = 10
TITLE_FONT_OFFSET_Y: int = 24

START_STATUS_OFFSET:   int = -30  # Because arcade 0,0 is at bottom left
INLINE_STATUS_OFFSET:  int = -20
STATUS_VALUE_X_OFFSET: int = 100

PropertyName  = NewType('PropertyName', str)
PropertyNames = NewType('PropertyNames', List[PropertyName])

LabelTextObjects = NewType('LabelTextObjects', List[Text])
ValueTextObjects = NewType('ValueTextObjects', List[Text])

class StatusConsoleSection(BaseSection):

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

        assert MessageConsoleProxy().initialized is True, 'The console proxy should have been set up at game startup'

        self._eventEngine:      EventEngine   = EventEngine(MessageConsoleProxy())
        self._statusProperties: PropertyNames = self._createStatusPropertyNameList()

        # --- Reusable Text Object Setup ---
        statusConsoleLabelX: int = round(self.left + TITLE_MARGIN_X)
        statusConsoleLabelY: int = (QUADRANT_GRID_HEIGHT + CONSOLE_SECTION_HEIGHT + COMMAND_SECTION_HEIGHT) - TITLE_FONT_OFFSET_Y - TITLE_MARGIN_Y

        self._titleText: Text = Text(
            text="Status Console",
            x=statusConsoleLabelX,
            y=statusConsoleLabelY,
            color=STATUS_TEXT_COLOR,
            font_size=SECTION_LABEL_FONT_SIZE,
            font_name=FIXED_WIDTH_FONT_NAME
        )

        self._labelTextObjects: LabelTextObjects = self._createStaticLabelTextObjects(statusConsoleLabelX=statusConsoleLabelX, statusConsoleLabelY=statusConsoleLabelY)
        self._valueTextObjects: ValueTextObjects = self._createDynamicValueTextObjects(statusConsoleLabelX=statusConsoleLabelX, statusConsoleLabelY=statusConsoleLabelY)

    def on_draw(self):
        """
        Remember arcade's 0,0 origin is lower left corner
        """
        self._titleText.draw()
        self.drawStatusLabels()
        self.drawStatusValues()
        self.drawDebug()

    def drawStatusLabels(self,):
        """
        Draws the pre-instantiated static labels.
        """
        for textObject in self._labelTextObjects:
            textObject.draw()

    def drawStatusValues(self):
        """
        Keep track of runningY so if we want to show internal values the appear below the reguarl values
        Additionally, if the status console grows or shrinks the internal values move
        """
        statusConsoleLabelX: int = round(self.left + TITLE_MARGIN_X)
        statusConsoleLabelY: int = (QUADRANT_GRID_HEIGHT + CONSOLE_SECTION_HEIGHT + COMMAND_SECTION_HEIGHT) - TITLE_FONT_OFFSET_Y - TITLE_MARGIN_Y

        labelX:   int = statusConsoleLabelX
        statusX:  int = labelX + STATUS_VALUE_X_OFFSET
        runningY: int = statusConsoleLabelY + START_STATUS_OFFSET

        statusPropertyNames: PropertyNames = self._statusProperties

        for index, propertyName in enumerate(statusPropertyNames):

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

            # Get the pre-instantiated text object for this index
            textObject: Text = self._valueTextObjects[index]
            textObject.text = propertyStr
            textObject.color = baseTextColor
            textObject.draw()

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

    def _createStatusPropertyNameList(self) -> PropertyNames:

        statusPropertyNames: PropertyNames = PropertyNames([])

        statusPropertyNames.append(PropertyName('shipCondition'))
        statusPropertyNames.append(PropertyName('starDate'))
        statusPropertyNames.append(PropertyName('currentQuadrantCoordinates'))
        statusPropertyNames.append(PropertyName('currentSectorCoordinates'))
        statusPropertyNames.append(PropertyName('energy'))
        statusPropertyNames.append(PropertyName('shieldEnergy'))
        statusPropertyNames.append(PropertyName('remainingGameTime'))
        statusPropertyNames.append(PropertyName('remainingKlingons'))
        statusPropertyNames.append(PropertyName('remainingCommanders'))
        statusPropertyNames.append(PropertyName('torpedoCount'))

        return statusPropertyNames

    def _createStaticLabelTextObjects(self, statusConsoleLabelX: int, statusConsoleLabelY: int) -> LabelTextObjects:
        """
        Create static label Text objects

        Args:
            statusConsoleLabelX:
            statusConsoleLabelY:

        Returns:    The label text objects
        """

        labelTextObjects: LabelTextObjects = LabelTextObjects([])
        runningY:         int              = statusConsoleLabelY + START_STATUS_OFFSET

        for labelText in StatusConsoleSection.statusLabels:
            textObject: Text = Text(
                text=labelText,
                x=statusConsoleLabelX,
                y=runningY,
                color=STATUS_TEXT_COLOR,
                font_size=STATUS_LABEL_FONT_SIZE,
                font_name=FIXED_WIDTH_FONT_NAME
            )
            labelTextObjects.append(textObject)
            runningY = runningY + INLINE_STATUS_OFFSET

        return labelTextObjects

    def _createDynamicValueTextObjects(self, statusConsoleLabelX: int, statusConsoleLabelY: int) -> ValueTextObjects:
        """

        Args:
            statusConsoleLabelX:
            statusConsoleLabelY:

        Returns:  The dynamic value text objects
        """

        valueTextObjects: ValueTextObjects = ValueTextObjects([])

        statusX:  int = statusConsoleLabelX + STATUS_VALUE_X_OFFSET
        runningY: int = statusConsoleLabelY + START_STATUS_OFFSET

        # We are running this loop N times, but we purposefully ignore the loop index.
        for _ in range(len(self._statusProperties)):
            textObject: Text = Text(
                text='',
                x=statusX,
                y=runningY,
                color=STATUS_TEXT_COLOR,
                font_size=STATUS_LABEL_FONT_SIZE,
                font_name=FIXED_WIDTH_FONT_NAME
            )
            valueTextObjects.append(textObject)
            runningY = runningY + INLINE_STATUS_OFFSET

        return valueTextObjects

    def __getTimeString(self, eventType: FutureEventType):

        fEvent: FutureEvent = self._eventEngine.getEvent(eventType)
        evtStr: str = f'{fEvent.starDate:.2f}'

        return evtStr
