
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from codeallybasic.SingletonV3 import SingletonV3

from pytrek.gui.AbstractMessageConsole import AbstractMessageConsole
from pytrek.gui.ConsoleMessageType import ConsoleMessageType

from pytrek.guiv2.MessageConsoleSection import MessageConsoleSection


Console = Union[AbstractMessageConsole, MessageConsoleSection]


class MessageConsoleProxy(metaclass=SingletonV3):
    """
    Various components need to display messages on the message
    console.  However, in the V2 version of the PyTrek UI, I converted
    the major game areas to sections as a way to isolate code.  This proxy
    is a singleton and early in game start up needs to be initialized
    with the actual MessageConsole section.

    Additionally, I want the old code that is still using
    A better way to do this would be for the various components to send
    a message.  The current version of arcade
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._console: Console = cast(Console, None)

    @property
    def initialized(self) -> bool:
        if self._console is None:
            return False
        return True

    def _consoleDisplay(self, console: Console):
        self._console = console

    # noinspection PyTypeChecker
    console = property(fget=None, fset=_consoleDisplay, doc='Write only property to set the appropriate console writer')

    def displayMessage(self, message: str, messageType: ConsoleMessageType = ConsoleMessageType.Normal):
        self._console.displayMessage(message=message, messageType=messageType)
