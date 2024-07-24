
from typing import Callable

from arcade.gui import UIManager
from arcade.gui import UIMessageBox

OK_BUTTON_TEXT:     str = 'Ok'
CANCEL_BUTTON_TEXT: str = 'Cancel'
OK_ANSWER:          str = OK_BUTTON_TEXT
CANCEL_ANSWER:      str = CANCEL_BUTTON_TEXT


class StdConfirmationDialog:
    """
    Just a way for me to isolate this underlying arcade component in case they
    change it
    """
    @classmethod
    def displayMessageBox(cls, uiManager: UIManager, msg: str, callback: Callable):
        """
        Displays a message box with a 'Ok' and 'Cancel' button to

        Args:
            uiManager:  The arcade ui manager to use
            msg: The message to display
            callback
        """
        messageBox: UIMessageBox = UIMessageBox(
            width=300,
            height=200,
            message_text=msg,
            buttons=(OK_BUTTON_TEXT, CANCEL_BUTTON_TEXT),
            callback=callback
        )
        uiManager.add(messageBox)
