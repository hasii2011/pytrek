
from logging import Logger
from logging import getLogger

from arcade import View
from arcade import Window
from arcade import draw_text
from arcade import start_render

from arcade.color import BLACK
from arcade.color import WHITE

from arcade import run as arcadeRun
from arcade import key as arcadeKey
from arcade import exit as arcadeExit


from pytrek.Constants import COMMAND_SECTION_HEIGHT
from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.ShipCondition import ShipCondition

from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceManager import DeviceManager
from pytrek.gui.BaseSection import BaseSection

from pytrek.gui.DeviceStatusSection import DeviceStatusSection
from pytrek.gui.MessageConsoleProxy import MessageConsoleProxy
from pytrek.gui.MessageConsoleSection import MessageConsoleSection

from tests.ProjectTestBase import ProjectTestBase

SCREEN_TITLE:   str = 'Test Fix Devices'
SECTION_HEIGHT: int = 100


class InputSection(BaseSection):
    """
    Self sizing and positioning within the game window
    """
    def __init__(self, **kwargs):

        self.inputLogger: Logger = getLogger(__name__)

        left:   int = 0
        bottom: int = COMMAND_SECTION_HEIGHT + CONSOLE_SECTION_HEIGHT + 5
        width:  int = self.window.width * 0.60
        height: int = SECTION_HEIGHT

        super().__init__(left=left, bottom=bottom, width=width, height=height, **kwargs)

        self._deviceManager: DeviceManager = DeviceManager()
        self._intelligence:  Intelligence  = Intelligence()
        self._opTime:        float         = 0
        self._starDate:      float         = self._intelligence.generateInitialStarDate()
        self._shipCondition: ShipCondition = ShipCondition.Green

    def on_draw(self):

        start_render()
        operationTimeValueX: int = self.left + 10
        operationTimeValueY: int = self.top  - 20

        draw_text(f'Operation time: {self._opTime} ', start_x=operationTimeValueX, start_y=operationTimeValueY, color=WHITE, font_size=12)

        startDateX: float = self.left + 10
        startDateY: float = self.top  - 40

        draw_text(f'Star date: {self._starDate} ', start_x=startDateX, start_y=startDateY, color=WHITE, font_size=12)

        startX: int = self.left + 10
        startY: int = self.bottom + 15
        draw_text(f'(Q)uit ', start_x=startX, start_y=startY, color=WHITE, font_size=12)

        opTimeX: int = startX + 80
        opTimeY: int = startY
        draw_text(f'opTime (1-9)', start_x=opTimeX, start_y=opTimeY, color=WHITE, font_size=12)

        fixCmdX: int = opTimeX + 140
        fixCmdY: int = opTimeY
        draw_text(f'(F)ix', start_x=fixCmdX, start_y=fixCmdY, color=WHITE, font_size=12)

        self.drawDebug()

    def on_key_press(self, pressedKey: int, modifiers: int):
        """
        Called whenever the user releases a previously pressed key.
        """
        if self._wasNumberPressed(pressedKey=pressedKey) is True:
            self._opTime = self._keyToValue(pressedKey)
        else:
            match pressedKey:
                case arcadeKey.Q:
                    arcadeExit()
                case arcadeKey.F:
                    self._deviceManager.fixDevices(starDate=self._starDate, opTime=self._opTime, shipCondition=self._shipCondition)
                case _:
                    self.inputLogger.warning('Huh')

    def _wasNumberPressed(self, pressedKey: int) -> bool:
        """
        Recognizes 1-9;  incrementing the star date by 0 makes no sense
        Args:
            pressedKey:  The arcade key that was pressed

        Returns:  `True` if between 1 and 9 inclusive, else `False`
        """

        ans: bool = False
        if arcadeKey.KEY_1 <= pressedKey <= arcadeKey.KEY_9:
            ans = True
        return ans

    def _keyToValue(self, pressedKey: int):
        """
        Assumes the arcade key values are numerically ascending
        Args:
            pressedKey:  The arcade key that was pressed

        Returns: A value between 1-9
        """
        return pressedKey - arcadeKey.KEY_0


class TestView(View):
    """
    The test view
    """

    def __init__(self):
        super().__init__()

        self._messageConsoleSection: MessageConsoleSection = MessageConsoleSection(left=0, bottom=COMMAND_SECTION_HEIGHT,
                                                                                   height=CONSOLE_SECTION_HEIGHT, width=SCREEN_WIDTH,
                                                                                   accept_keyboard_events=False
                                                                                   )

        # Create proxy and inject the console
        self._messageConsoleProxy = MessageConsoleProxy()
        self._messageConsoleProxy.console = self._messageConsoleSection

        self._deviceStatusSection:   DeviceStatusSection = DeviceStatusSection(modal=False)
        self._inputSection:          InputSection        = InputSection()

        self.section_manager.add_section(self._inputSection)
        self.section_manager.add_section(self._messageConsoleSection)
        self.section_manager.add_section(self._deviceStatusSection)

        #
        # Set these to test status colors:
        #
        self._devices: DeviceManager = DeviceManager()

        self._devices.setDeviceStatus(deviceType=DeviceType.ImpulseEngines, deviceStatus=DeviceStatus.Damaged)
        self._devices.setDeviceDamage(deviceType=DeviceType.ImpulseEngines, damageValue=5)

        self._devices.setDeviceStatus(deviceType=DeviceType.Transporter, deviceStatus=DeviceStatus.Down)
        self._devices.setDeviceDamage(deviceType=DeviceType.Transporter, damageValue=6)

        self._devices.setDeviceStatus(deviceType=DeviceType.DeathRay, deviceStatus=DeviceStatus.Down)
        self._devices.setDeviceDamage(deviceType=DeviceType.DeathRay, damageValue=2.0)

    def on_draw(self):
        pass


def main():

    ProjectTestBase.setUpLogging()

    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    arcadeWindow.background_color = BLACK
    arcadeWindow.clear()

    testView: TestView = TestView()
    arcadeWindow.show_view(testView)

    arcadeRun()


if __name__ == "__main__":
    main()
