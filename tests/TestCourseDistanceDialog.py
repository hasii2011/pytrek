from arcade import Window
from arcade import color

from arcade import run as arcadeRun

from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.gui.CourseDistanceDialog import CourseDistanceAnswer

from pytrek.gui.CourseDistanceDialog import CourseDistanceDialog
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase

VIEW_WIDTH:  int = SCREEN_WIDTH
VIEW_HEIGHT: int = SCREEN_HEIGHT


def main():
    """
    Main method
    """
    TestBase.setUpLogging()
    SettingsCommon.determineSettingsLocation()

    arcadeWindow: Window = Window(title='Test Course & Distance', width=VIEW_WIDTH, height=VIEW_HEIGHT)
    arcadeWindow.background_color = color.WHITE
    arcadeWindow.clear()
    arcadeWindow.set_exclusive_keyboard(exclusive=True)

    testCDView:  CourseDistanceDialog = CourseDistanceDialog(completeCallback=completeCallback)

    arcadeWindow.show_view(testCDView)

    arcadeRun()


def completeCallback(answer: CourseDistanceAnswer):

    print(f'{answer=}')


if __name__ == "__main__":
    main()
