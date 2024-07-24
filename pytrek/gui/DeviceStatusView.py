
from logging import Logger
from logging import getLogger
from typing import Callable

from arcade import View
from arcade import color
from arcade import start_render
from arcade import draw_line
from arcade import draw_text

from arcade.gui import UIManager

from pytrek.Constants import SCREEN_HEIGHT

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices

X_MARGIN:        float = 190.0
Y_MARGIN:        float = 100.0

DEVICE_Y:        float = SCREEN_HEIGHT - Y_MARGIN

DEVICE_TYPE_X:   float = X_MARGIN
DEVICE_DAMAGE_X: float = DEVICE_TYPE_X + 210
DEVICE_STATUS_X: float = DEVICE_DAMAGE_X + 100

EVENT_TYPE_X:           float = DEVICE_STATUS_X + 120
EVENT_DATE_X:           float = EVENT_TYPE_X    + 210

EVENT_TYPE_Y:           float = DEVICE_Y

EVENT_HEADER_COLOR:      tuple[int, int, int] = color.WHITE
DEVICE_HEADER_COLOR:     tuple[int, int, int] = color.WHITE
DEVICE_DETAIL_COLOR:     tuple[int, int, int] = color.WHITE

EVENT_HEADER_FONT_SIZE:  int = 12
DEVICE_HEADER_FONT_SIZE: int = 12
DEVICE_DETAIL_FONT_SIZE: int = 10

HEADER_Y:        float = DEVICE_Y - 10

SEPARATOR_END_X: float = DEVICE_STATUS_X + 50


class DeviceStatusView(View):
    """
    Report status of ship systems
    """
    def __init__(self, viewCompleteCallback: Callable):

        self.logger: Logger = getLogger(__name__)
        super().__init__()
        self._viewCompleteCallback: Callable = viewCompleteCallback

        self._devices:   Devices   = Devices()
        self._uiManager: UIManager = UIManager()

        self._uiManager.enable()

    def on_draw(self):
        """
        Draw this view
        """
        start_render()
        self._uiManager.draw()

        self._drawHeader()
        self._drawDevicesStatus()

    def _drawHeader(self):

        draw_text(f'Device type', DEVICE_TYPE_X, DEVICE_Y,   DEVICE_HEADER_COLOR, DEVICE_HEADER_FONT_SIZE)
        draw_text(f'Damage',      DEVICE_DAMAGE_X, DEVICE_Y, DEVICE_HEADER_COLOR, DEVICE_HEADER_FONT_SIZE)
        draw_text(f'Status',      DEVICE_STATUS_X, DEVICE_Y, DEVICE_HEADER_COLOR, DEVICE_HEADER_FONT_SIZE)

        draw_line(start_x=DEVICE_TYPE_X, end_x=SEPARATOR_END_X, start_y=HEADER_Y, end_y=HEADER_Y, color=color.WHITE, line_width=2)

    def _drawDevicesStatus(self):

        # # Separator line

        # Devices themselves
        y: float = DEVICE_Y - 20

        for deviceType in DeviceType:
            y -= 20
            device:       Device       = self._devices.getDevice(deviceType=deviceType)
            damage:       float        = device.damage
            deviceStatus: DeviceStatus = device.deviceStatus

            draw_text(f' {deviceType}',   DEVICE_TYPE_X, y,   DEVICE_DETAIL_COLOR, DEVICE_DETAIL_FONT_SIZE)
            draw_text(f' {damage:.2f}',   DEVICE_DAMAGE_X, y, DEVICE_DETAIL_COLOR, DEVICE_DETAIL_FONT_SIZE)
            draw_text(f' {deviceStatus}', DEVICE_STATUS_X, y, DEVICE_DETAIL_COLOR, DEVICE_DETAIL_FONT_SIZE)

        footerY: float = y - 5
        draw_line(start_x=DEVICE_TYPE_X, end_x=SEPARATOR_END_X, start_y=footerY, end_y=footerY, color=color.WHITE, line_width=2)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        If the user presses the mouse button, go back to the game
        """
        self._viewCompleteCallback()
