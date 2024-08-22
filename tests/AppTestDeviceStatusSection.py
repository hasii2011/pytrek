
from arcade import View
from arcade import Window
from arcade.color import BLACK

from arcade import run as arcadeRun

from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices

from pytrek.guiv2.DeviceStatusSection import DeviceStatusSection
from tests.DrawTextSection import DrawTextSection

from tests.ProjectTestBase import ProjectTestBase

SCREEN_TITLE: str = 'Test Device Status Section'


class TestView(View):
    """
    The test view
    """

    def __init__(self):
        super().__init__()

        self._drawTextSection:     DrawTextSection     = DrawTextSection(enabled=True)
        self._deviceStatusSection: DeviceStatusSection = DeviceStatusSection(enabled=True)
        self.section_manager.add_section(self._drawTextSection)
        self.section_manager.add_section(self._deviceStatusSection)

        #
        # Set these to test status colors:
        #
        self._devices: Devices = Devices()

        self._devices.setDeviceStatus(deviceType=DeviceType.ImpulseEngines, deviceStatus=DeviceStatus.Damaged)
        self._devices.setDeviceDamage(deviceType=DeviceType.ImpulseEngines, damageValue=20)

        self._devices.setDeviceStatus(deviceType=DeviceType.Transporter, deviceStatus=DeviceStatus.Down)
        self._devices.setDeviceDamage(deviceType=DeviceType.Transporter, damageValue=100)

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
