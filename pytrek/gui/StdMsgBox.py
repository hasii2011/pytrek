from arcade.gui import UIManager
from arcade.gui import UIMessageBox


class StdMsgBox:
    """
    Just a way for me to isolate this underlying arcade component in case they
    change it
    """
    @staticmethod
    def displayMessageBox(uiManager: UIManager, msg: str):
        """
        Displays a message box with a single 'Ok' button to dismiss

        Args:
            uiManager:  The arcade ui manager to use
            msg: The message to display
        """
        messageBox: UIMessageBox = UIMessageBox(
            width=300,
            height=200,
            message_text=msg,
            buttons=["Ok"]
        )
        uiManager.add(messageBox)
