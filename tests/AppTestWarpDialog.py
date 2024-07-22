from arcade import Window
from arcade import color

from arcade import run as arcadeRun

from pytrek.gui.WarpDialog import DialogAnswer
from pytrek.gui.WarpDialog import WarpDialog
from pytrek.gui.WarpDialog import WarpTravelAnswer
from tests.ProjectTestBase import ProjectTestBase

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Test Warp Dialog"


def completeCallback(warpTravelAnswer: WarpTravelAnswer):
    import os
    if warpTravelAnswer.dialogAnswer == DialogAnswer.Cancelled:
        # noinspection PyUnresolvedReferences
        # noinspection PyProtectedMember
        os._exit(0)
    else:
        print(f'{warpTravelAnswer=}')


def main():

    ProjectTestBase.setUpLogging()

    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    arcadeWindow.background_color = color.BLACK
    arcadeWindow.clear()

    warpDialog:  WarpDialog = WarpDialog(window=arcadeWindow, completeCallback=completeCallback)

    arcadeWindow.show_view(warpDialog)

    arcadeRun()


if __name__ == "__main__":
    main()
