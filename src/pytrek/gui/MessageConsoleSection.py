
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from arcade.color import RED
from arcade.color import WHITE

from arcade import Text
from arcade.types import Color

from pytrek.Constants import COMMAND_SECTION_HEIGHT
from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_NAME

from pytrek.gui.ConsoleMessageType import ConsoleMessageType
from pytrek.gui.BaseSection import BaseSection


@dataclass
class MessageLine:
    message: str = ''
    textColor: Color = WHITE


MessageLines = NewType('MessageLines', List[MessageLine])

TextObjects = NewType('TextObjects', List[Text])


class MessageConsoleSection(BaseSection):
    """
    This section caches the messages in a buffer.  It uses a set of prebuilt
    text object to display them
    """

    MAX_LINES:                 int = 13

    CONSOLE_FONT_SIZE:         int = 10
    BETWEEN_LINE_MARGIN:       int = 3
    EXTRA_FIRST_LINE_Y_OFFSET: int = 5
    FIRST_LINE_Y:              int = (CONSOLE_SECTION_HEIGHT + COMMAND_SECTION_HEIGHT) - CONSOLE_FONT_SIZE - BETWEEN_LINE_MARGIN - EXTRA_FIRST_LINE_Y_OFFSET
    X_FIXED:                   int = 5
    Y_DECREMENT:               int = CONSOLE_FONT_SIZE + BETWEEN_LINE_MARGIN

    CONSOLE_TEXT_COLOR = WHITE

    def __init__(self, left: int, bottom: int, width: int, height: int, **kwargs):

        self.logger: Logger = getLogger(__name__)

        super().__init__(left=left, bottom=bottom, width=width, height=height, **kwargs)

        self._statusLines: MessageLines = MessageLines([])

        self._textObjects: TextObjects = self._preCreateTextObjects()

        # runningY: int = MessageConsoleSection.FIRST_LINE_Y
        # for _ in range(MessageConsoleSection.MAX_LINES):
        #     textObj = Text(
        #         text='',
        #         x=MessageConsoleSection.X_FIXED,
        #         y=runningY,
        #         color=WHITE,
        #         font_size=MessageConsoleSection.CONSOLE_FONT_SIZE,
        #         font_name=FIXED_WIDTH_FONT_NAME
        #     )
        #     self._textObjects.append(textObj)
        #     runningY -= MessageConsoleSection.Y_DECREMENT

    def displayMessage(self, message: str, messageType: ConsoleMessageType = ConsoleMessageType.Normal):
        """
        Simply adds the new message to the message buffer

        Args:
            message:  New message to display
            messageType: How to display the message
        """
        if len(self._statusLines) == MessageConsoleSection.MAX_LINES:
            self._statusLines.pop(0)

        msgLine: MessageLine = MessageLine(message=message)
        if messageType == ConsoleMessageType.Warning:
            msgLine.textColor = RED

        self._statusLines.append(msgLine)

    def on_draw(self):
        """
        Simply apply the current messages to the prebuilt text objects
        """

        for index, msg in enumerate(self._statusLines):
            textObj = self._textObjects[index]
            textObj.text = msg.message
            textObj.color = msg.textColor
            textObj.draw()

        self.drawDebug()

    def _preCreateTextObjects(self) -> TextObjects:

        textObjects: TextObjects = TextObjects([])
        runningY:   int          = MessageConsoleSection.FIRST_LINE_Y

        for _ in range(MessageConsoleSection.MAX_LINES):
            textObj = Text(
                text='',
                x=MessageConsoleSection.X_FIXED,
                y=runningY,
                color=WHITE,
                font_size=MessageConsoleSection.CONSOLE_FONT_SIZE,
                font_name=FIXED_WIDTH_FONT_NAME
            )
            textObjects.append(textObj)
            runningY -= MessageConsoleSection.Y_DECREMENT

        return textObjects
