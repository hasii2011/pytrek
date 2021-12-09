from logging import Logger
from logging import getLogger

from pytrek.gui.AbstractMessageConsole import AbstractMessageConsole


class LogMessageConsole(AbstractMessageConsole):
    """
    Used by the unit tests to inject it TestFutureEventHandlers
    """

    # noinspection SpellCheckingInspection
    def init(self, *args, **kwds):
        self.logger: Logger = getLogger(__name__)

    def draw(self):
        pass

    def displayMessage(self, message: str):
        """
        Args:
            message:  New message to display
        """
        self.logger.info(message)