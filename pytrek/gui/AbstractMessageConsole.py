
from hasiihelper.Singleton import Singleton

from pytrek.gui.ConsoleMessageType import ConsoleMessageType


class AbstractMessageConsole(Singleton):

    # noinspection SpellCheckingInspection
    def init(self, *args, **kwargs):
        pass

    def draw(self):
        pass

    def displayMessage(self, message: str, messageType: ConsoleMessageType = ConsoleMessageType.Normal):
        """
        Args:
            message:  New message to display
            messageType: How to display the message
        """
