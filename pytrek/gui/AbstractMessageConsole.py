
from codeallybasic.SingletonV3 import SingletonV3

from pytrek.gui.ConsoleMessageType import ConsoleMessageType


class AbstractMessageConsole(metaclass=SingletonV3):

    def __init__(self, *args, **kwargs):
        pass

    def draw(self):
        pass

    def displayMessage(self, message: str, messageType: ConsoleMessageType = ConsoleMessageType.Normal):
        """
        Args:
            message:  New message to display
            messageType: How to display the message
        """
        pass
