from arcade import SectionManager
from arcade import View
from arcade import Window
from arcade import color

from arcade import run as arcadeRun

from src.pytrek.Constants import SCREEN_HEIGHT
from src.pytrek.Constants import SCREEN_WIDTH
from src.pytrek.gui.VatoLocoTextSection import VatoLocoTextSection
from tests.ProjectTestBase import ProjectTestBase

SCREEN_TITLE:  str = "Test Vato Loco"


class TestView(View):
    """
    The test view
    """

    def __init__(self):
        super().__init__()
        self.sectionManager: SectionManager = SectionManager(self)

        self._textInputSection: VatoLocoTextSection = VatoLocoTextSection(left=0, bottom=0, callback=self._returnPressedCallback)

        self.sectionManager.add_section(self._textInputSection)

    def _returnPressedCallback(self, value: str):
        print(f'{value=}')

    def on_draw(self):
        self.clear()

    def on_show_view(self):
        self.sectionManager.enable()

    def on_hide_view(self):
        self.sectionManager.disable()


def main():

    ProjectTestBase.setUpLogging()

    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    arcadeWindow.background_color = color.BLACK
    arcadeWindow.clear()

    testView: TestView = TestView()
    arcadeWindow.show_view(testView)

    arcadeRun()


if __name__ == "__main__":
    main()
