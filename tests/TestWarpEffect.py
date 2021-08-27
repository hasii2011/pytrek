

from arcade import Window

from arcade import run as arcadeRun
from arcade import schedule
# from arcade import unschedule

from pytrek.gui.WarpEffect import WarpEffect

from pytrek.settings.SettingsCommon import SettingsCommon
from tests.TestBase import TestBase

SCREEN_WIDTH:  int = 800
SCREEN_HEIGHT: int = 600
SCREEN_TITLE:  str = "Test Warp Effect"


class WarpEffectRunner:

    def __init__(self):
        arcadeWindow: Window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        warpEffect: WarpEffect = WarpEffect(screenWidth=SCREEN_WIDTH, screenHeight=SCREEN_HEIGHT)

        arcadeWindow.set_exclusive_keyboard(exclusive=True)
        arcadeWindow.show_view(warpEffect)

        schedule(function_pointer=self.checkEffectComplete, interval=1.0)
        warpEffect.setup()

        self._warpEffect: WarpEffect = warpEffect

    def run(self):
        arcadeRun()

    def checkEffectComplete(self, deltaTime: float):

        effectComplete: bool = self._warpEffect.isEffectComplete()
        print(f'Checking {deltaTime} {effectComplete=}')
        # if effectComplete is True:
        #     print('Quit')
        #     unschedule(self.checkEffectComplete)


def main():

    TestBase.setUpLogging()
    SettingsCommon.determineSettingsLocation()

    warpEffectRunner: WarpEffectRunner = WarpEffectRunner()

    warpEffectRunner.run()


if __name__ == "__main__":
    main()
