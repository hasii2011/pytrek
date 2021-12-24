from arcade import Window
from arcade import color

from arcade import run as arcadeRun
from pytrek.gui.WarpDialog import WarpDialog

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Test Warp Dialog"


def main():
    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    arcadeWindow.background_color = color.BLACK
    arcadeWindow.clear()

    warpDialog:  WarpDialog = WarpDialog(window=arcadeWindow)

    arcadeWindow.show_view(warpDialog)

    arcadeRun()


if __name__ == "__main__":
    main()