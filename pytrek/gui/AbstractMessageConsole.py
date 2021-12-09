
from pytrek.Singleton import Singleton


class AbstractMessageConsole(Singleton):

    # noinspection SpellCheckingInspection
    def init(self, *args, **kwds):
        pass

    def draw(self):
        pass

    def displayMessage(self, message: str):
        """
        Args:
            message:  New message to display
        """
