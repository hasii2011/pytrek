from arcade import Window
from arcade import color

from arcade import run as arcadeRun

from pytrek.gui.CourseDistanceDialog import CourseDistanceDialog
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase

VIEW_WIDTH:  int = 800
VIEW_HEIGHT: int = 600


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

    testCDView:     CourseDistanceDialog = CourseDistanceDialog()

    arcadeWindow.show_view(testCDView)

    arcadeRun()


if __name__ == "__main__":
    main()
