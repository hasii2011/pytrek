
from typing import List

from logging import Logger
from logging import getLogger

from arcade import draw_text
from arcade.color import WHITE

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_NAME
from pytrek.Singleton import Singleton


class MessageConsole(Singleton):

    MAX_LINES:                 int = 13

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

        runningY: int = MessageConsole.FIRST_LINE_Y
        for msg in self._statusLines:
            draw_text(msg, MessageConsole.X_FIXED, runningY, color=MessageConsole.CONSOLE_TEXT_COLOR,
                      font_size=MessageConsole.CONSOLE_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)

            runningY -= MessageConsole.Y_DECREMENT

    def displayMessage(self, message: str):
        """
        Simply adds the new message to the message buffer
        Args:
            message:  New message to display
        """
        if len(self._statusLines) == MessageConsole.MAX_LINES:
            self._statusLines.pop(0)

        self._statusLines.append(message)
