from arcade import Window
from arcade import color

from arcade import run as arcadeRun

from pytrek.gui.HelpView import HelpView

from pytrek.settings.SettingsCommon import SettingsCommon
from tests.TestBase import TestBase

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Test Help View"


def main():

    TestBase.setUpLogging()
    SettingsCommon.determineSettingsLocation()

    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    # arcadeWindow.background_color = color.BLUE
    arcadeWindow.clear()

    helpView:  HelpView = HelpView(window=arcadeWindow)

    arcadeWindow.show_view(helpView)

    arcadeRun()


if __name__ == "__main__":
    main()
