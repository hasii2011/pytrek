
from arcade import Window
from arcade import color

from arcade import run as arcadeRun

from pytrek.gui.HelpView import HelpView


from tests.ProjectTestBase import ProjectTestBase

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Test Help View"


def completeCallback():

    import os

    print(f'Help View has been terminated')
    # noinspection PyUnresolvedReferences
    # noinspection PyProtectedMember
    os._exit(0)


def main():

    ProjectTestBase.setUpLogging()

    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    arcadeWindow.background_color = color.BLUE_YONDER

    arcadeWindow.clear()

    helpView:  HelpView = HelpView(completeCallback=completeCallback)

    arcadeWindow.show_view(helpView)

    arcadeRun()


if __name__ == "__main__":
    main()
