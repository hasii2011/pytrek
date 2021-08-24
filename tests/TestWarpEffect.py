

from arcade import Window

from arcade import run as arcadeRun

from pytrek.gui.WarpEffect import WarpEffect

from pytrek.settings.SettingsCommon import SettingsCommon
from tests.TestBase import TestBase

SCREEN_WIDTH:  int = 800
SCREEN_HEIGHT: int = 600
SCREEN_TITLE:  str = "Test Warp Effect"


def main():

    TestBase.setUpLogging()
    SettingsCommon.determineSettingsLocation()

    arcadeWindow:   Window     = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    warpEffectView: WarpEffect = WarpEffect(screenWidth=SCREEN_WIDTH, screenHeight=SCREEN_HEIGHT)

    arcadeWindow.set_exclusive_keyboard(exclusive=True)
    arcadeWindow.show_view(warpEffectView)

    warpEffectView.setup()
    arcadeRun()


if __name__ == "__main__":
    main()
