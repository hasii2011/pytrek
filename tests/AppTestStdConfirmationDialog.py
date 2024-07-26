from logging import Logger
from logging import getLogger

from arcade import View
from arcade import Window
from arcade import color

from arcade import run as arcadeRun
from arcade import key as arcadeKey

from arcade import set_background_color
from arcade import start_render
from arcade.gui import UIManager

from pytrek.LocateResources import LocateResources

from pytrek.gui.dialogs.StdConfirmationDialog import StdConfirmationDialog

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
SCREEN_TITLE = "Test Confirmation Dialog"


class AppTestStdConfirmationDialog(View):
    """
    Use this as a template when setting up application test programs
    """
    ETX_COLOR = color.WHITE

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        set_background_color(color.BLACK)
        self._uiManager: UIManager = UIManager()
        self._uiManager.enable()

    def on_draw(self):
        start_render()
        self._uiManager.draw()

    def on_key_release(self, releasedKey: int, key_modifiers: int):
        """
        Called whenever the user releases a previously pressed key.
        """
        if releasedKey == arcadeKey.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)
        elif releasedKey == arcadeKey.C:
            StdConfirmationDialog.displayMessageBox(uiManager=self._uiManager, msg='Save current game progress?', callback=self._confirmationCallback)

    def _confirmationCallback(self, buttonText: str):
        self.logger.warning(f'You pressed {buttonText}')


def main():

    LocateResources.setupSystemLogging()

    arcadeWindow: Window     = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    view: AppTestStdConfirmationDialog = AppTestStdConfirmationDialog()

    arcadeWindow.set_exclusive_keyboard(exclusive=False)
    arcadeWindow.show_view(view)

    arcadeRun()


if __name__ == "__main__":
    main()
