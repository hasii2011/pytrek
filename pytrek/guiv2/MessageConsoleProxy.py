
from typing import cast

from logging import Logger
from logging import getLogger

from codeallybasic.SingletonV3 import SingletonV3

from pytrek.gui.ConsoleMessageType import ConsoleMessageType

from pytrek.gui.MessageConsoleSection import MessageConsoleSection


class MessageConsoleProxy(metaclass=SingletonV3):
    """
    Various components need to display messages on the message
    console.  However, in the V2 version of the PyTrek UI, I converted
    the major game areas to sections as a way to isolate code.  This proxy
    is a singleton and early in game start up needs to be initialized
    with the actual MessageConsole section.
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._console: MessageConsoleSection = cast(MessageConsoleSection, None)

    @property
    def initialized(self) -> bool:
        if self._console is None:
            return False
        return True

    def _consoleDisplay(self, console: MessageConsoleSection):
        self._console = console

    # noinspection PyTypeChecker
    console = property(fget=None, fset=_consoleDisplay, doc='Write only property to set the appropriate console writer')

    def displayMessage(self, message: str, messageType: ConsoleMessageType = ConsoleMessageType.Normal):
        self._console.displayMessage(message=message, messageType=messageType)
