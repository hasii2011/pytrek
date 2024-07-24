
from arcade import Window
from arcade import color

from arcade import run as arcadeRun
from arcade import exit as arcadeExit

from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.gui.DeviceStatusView import DeviceStatusView

from tests.ProjectTestBase import ProjectTestBase

SCREEN_TITLE  = "Test Device Status View"


def viewCompleteCallback():

    print(f'View complete')
    arcadeExit()


def main():

    ProjectTestBase.setUpLogging()

    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    arcadeWindow.background_color = color.BLUE_YONDER

    arcadeWindow.clear()

    helpView:  DeviceStatusView = DeviceStatusView(viewCompleteCallback=viewCompleteCallback)

    arcadeWindow.show_view(helpView)

    arcadeRun()


if __name__ == "__main__":
    main()
