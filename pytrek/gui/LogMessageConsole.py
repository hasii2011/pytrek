
from logging import Logger
from logging import getLogger

from pytrek.gui.AbstractMessageConsole import AbstractMessageConsole
from pytrek.gui.ConsoleMessageType import ConsoleMessageType


class LogMessageConsole(AbstractMessageConsole):
    """
    Used by the unit tests to inject it TestFutureEventHandlers
    """
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def draw(self):
        pass

    def displayMessage(self, message: str, messageType: ConsoleMessageType = ConsoleMessageType.Normal):
        """
        Args:
            message:  New message to display
            messageType: How to display the message
        """
        if messageType == ConsoleMessageType.Normal:
            self.logger.info(message)
        elif messageType == ConsoleMessageType.Warning:
            self.logger.warning(message)
        else:
            self.logger.error(message)
