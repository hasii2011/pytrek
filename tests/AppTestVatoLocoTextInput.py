from arcade import View
from arcade import Window
from arcade import color

from arcade import run as arcadeRun
from arcade import start_render

from pytrek.guiv2.VatoLocoTextInput import VatoLocoTextInput
from tests.ProjectTestBase import ProjectTestBase

SCREEN_WIDTH:  int  = 800
SCREEN_HEIGHT: int = 600
SCREEN_TITLE:  str = "Test Vato Loco"


class TestView(View):
    """
    The test view
    """

    def __init__(self):
        super().__init__()

        self._textInputSection: VatoLocoTextInput = VatoLocoTextInput(left=0, bottom=0, callback=self._returnPressedCallback)

        self.section_manager.add_section(self._textInputSection)

    def _returnPressedCallback(self, value: str):
        print(f'{value=}')

    def on_draw(self):
        start_render()


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
