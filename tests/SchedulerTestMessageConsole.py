
from typing import List

from logging import Logger
from logging import getLogger

from arcade import draw_text
from arcade.color import WHITE

from pytrek.Constants import FIXED_WIDTH_FONT_NAME

from pytrek.gui.AbstractMessageConsole import AbstractMessageConsole
from pytrek.gui.ConsoleMessageType import ConsoleMessageType


class SchedulerTestMessageConsole(AbstractMessageConsole):
    """
    For use by the TestEventEngineScheduler;  Differs from game version only by the console size
    """

    MAX_LINES:                 int = 8

    CONSOLE_HEIGHT:            int = 85
    CONSOLE_FONT_SIZE:         int = 10
    BETWEEN_LINE_MARGIN:       int = 3
    EXTRA_FIRST_LINE_Y_OFFSET: int = 5
    FIRST_LINE_Y:              int = CONSOLE_HEIGHT - CONSOLE_FONT_SIZE - BETWEEN_LINE_MARGIN - EXTRA_FIRST_LINE_Y_OFFSET
    X_FIXED:                   int = 5
    Y_DECREMENT:               int = CONSOLE_FONT_SIZE + BETWEEN_LINE_MARGIN

    CONSOLE_TEXT_COLOR = WHITE

    # noinspection SpellCheckingInspection
    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        self._statusLines: List[str] = []

    def draw(self):

        runningY: int = SchedulerTestMessageConsole.FIRST_LINE_Y
        for msg in self._statusLines:
            draw_text(msg, SchedulerTestMessageConsole.X_FIXED, runningY, color=SchedulerTestMessageConsole.CONSOLE_TEXT_COLOR,
                      font_size=SchedulerTestMessageConsole.CONSOLE_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            runningY -= SchedulerTestMessageConsole.Y_DECREMENT

    def displayMessage(self, message: str, messageType: ConsoleMessageType = ConsoleMessageType.Normal):
        """
        Simply adds the new message to the message buffer
        Args:
            message:  New message to display
            messageType: How to display the message

        """
        if len(self._statusLines) == SchedulerTestMessageConsole.MAX_LINES:
            self._statusLines.pop(0)

        self._statusLines.append(message)
