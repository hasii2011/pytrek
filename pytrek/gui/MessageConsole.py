
from typing import List

from dataclasses import dataclass

from logging import Logger
from logging import getLogger
from typing import Tuple

from arcade import draw_text
from arcade.color import WHITE
from arcade.color import RED

from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_NAME

from pytrek.gui.AbstractMessageConsole import AbstractMessageConsole
from pytrek.gui.ConsoleMessageType import ConsoleMessageType


@dataclass
class MessageLine:
    message: str = ''
    textColor: Tuple[int, int, int] = WHITE


class MessageConsole(AbstractMessageConsole):

    MAX_LINES:                 int = 13

    CONSOLE_FONT_SIZE:         int = 10
    BETWEEN_LINE_MARGIN:       int = 3
    EXTRA_FIRST_LINE_Y_OFFSET: int = 5
    FIRST_LINE_Y:              int = CONSOLE_SECTION_HEIGHT - CONSOLE_FONT_SIZE - BETWEEN_LINE_MARGIN - EXTRA_FIRST_LINE_Y_OFFSET
    X_FIXED:                   int = 5
    Y_DECREMENT:               int = CONSOLE_FONT_SIZE + BETWEEN_LINE_MARGIN

    CONSOLE_TEXT_COLOR = WHITE

    def __init__(self):
        super().__init__()

        self.logger:       Logger = getLogger(__name__)
        self._statusLines: List[MessageLine] = []

    def draw(self):

        runningY: int = MessageConsole.FIRST_LINE_Y
        for msg in self._statusLines:
            draw_text(msg.message, MessageConsole.X_FIXED, runningY,
                      color=msg.textColor,
                      font_size=MessageConsole.CONSOLE_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            runningY -= MessageConsole.Y_DECREMENT

    def displayMessage(self, message: str, messageType: ConsoleMessageType = ConsoleMessageType.Normal):
        """
        Simply adds the new message to the message buffer
        Args:
            message:  New message to display
            messageType: How to display the message
        """
        if len(self._statusLines) == MessageConsole.MAX_LINES:
            self._statusLines.pop(0)

        msgLine: MessageLine = MessageLine(message=message)
        if messageType == ConsoleMessageType.Warning:
            msgLine.textColor = RED

        self._statusLines.append(msgLine)
