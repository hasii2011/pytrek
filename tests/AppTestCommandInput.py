
from arcade import SectionManager
from arcade import View
from arcade import Window
from arcade import color

from arcade import run as arcadeRun

from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.gui.CommandInputSection import CommandInputSection
from tests.ProjectTestBase import ProjectTestBase

screenTitle: str = 'Test Command Input'


class AppTestCommandInput(View):
    """
    The test view for CommandInputSection
    """

    def __init__(self):
        super().__init__()
        self.sectionManager: SectionManager = SectionManager(self)

        self._commandInputSection: CommandInputSection = CommandInputSection(left=0, bottom=1, commandEnteredCallback=self._commandEnteredCallback)

        self.sectionManager.add_section(self._commandInputSection)

    def _commandEnteredCallback(self, value: str):
        print(f'Captured command: {value}')

    def on_draw(self):
        self.clear()

    def on_show_view(self):
        self.sectionManager.enable()

    def on_hide_view(self):
        self.sectionManager.disable()


def main():

    ProjectTestBase.setUpLogging()

    arcadeWindow: Window = Window(title=screenTitle, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    arcadeWindow.background_color = color.BLACK
    arcadeWindow.clear()

    testView: AppTestCommandInput = AppTestCommandInput()
    arcadeWindow.show_view(testView)

    arcadeRun()


if __name__ == '__main__':
    main()
