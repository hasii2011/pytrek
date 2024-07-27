
from arcade import Window
from arcade import color

from arcade import run as arcadeRun
from arcade import exit as arcadeExit

from pytrek.gui.dialogs.DlgConstants import DialogAnswer
from pytrek.gui.dialogs.RestDialog import RestAnswer
from pytrek.gui.dialogs.RestDialog import RestDialog

from tests.ProjectTestBase import ProjectTestBase

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Test Rest Dialog"


def completeCallback(restAnswer: RestAnswer):
    if restAnswer.dialogAnswer == DialogAnswer.Cancelled:
        arcadeExit()
    else:
        print(f'{restAnswer=}')


def main():

    ProjectTestBase.setUpLogging()

    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    arcadeWindow.background_color = color.BLACK
    arcadeWindow.clear()

    restDialog:  RestDialog = RestDialog(completeCallback=completeCallback)

    arcadeWindow.show_view(restDialog)

    arcadeRun()


if __name__ == "__main__":
    main()
