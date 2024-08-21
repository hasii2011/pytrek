
from logging import Logger
from logging import getLogger

from arcade.color import RED
from arcade.color import WHITE
from arcade.color import YELLOW

from arcade import draw_text
from arcade import draw_line
from arcade import start_render

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices

from pytrek.guiv2.BaseSection import BaseSection

ColorType = tuple[int, int, int]

EVENT_HEADER_COLOR:      ColorType = WHITE
DEVICE_HEADER_COLOR:     ColorType = WHITE
DEVICE_DETAIL_COLOR:     ColorType = WHITE

STATUS_NORMAL_COLOR:   ColorType = WHITE
STATUS_DOWN_COLOR:     ColorType = RED
STATUS_DAMAGED_COLOR:  ColorType = YELLOW

EVENT_HEADER_FONT_SIZE:  int = 12
DEVICE_HEADER_FONT_SIZE: int = 12
DEVICE_DETAIL_FONT_SIZE: int = 10

SECTION_HEIGHT:     int = 420

LINE_MARGIN_LEFT:    int = 30
LINE_MARGIN_RIGHT:   int = 160
HEADER_MARGIN_LEFT:  int = 45
TEXT_TOP_OFFSET:     int = 20
TOP_LINE_TOP_OFFSET: int = 40
TYPE_HEADER_X_GAP:   int = 0
STATUS_HEADER_X_GAP: int = 15

DEVICE_STATUS_LINE_GAP: int = 17
FOOTER_GAP:             int = 15

DEVICE_TYPE_HEADER: str = 'Device Type'
DAMAGE_HEADER:      str = 'Damage'
STATUS_HEADER:      str = 'Status'


class DeviceStatusSection(BaseSection):
    """
    Self sizing and positioning within the game window
    """
    def __init__(self, **kwargs):
        left:   int = self.window.width * 0.40
        bottom: int = SECTION_HEIGHT
        width:  int = self.window.width * 0.60
        height: int = SECTION_HEIGHT

        super().__init__(left=left, bottom=bottom, width=width, height=height, modal=True, **kwargs)

        self.logger: Logger = getLogger(__name__)

        self._devices:   Devices   = Devices()

        self._deviceTypeHeaderX:   int = self.left + HEADER_MARGIN_LEFT
        self._deviceTypeHeaderY:   int = self.bottom + self.height - TEXT_TOP_OFFSET
        self._deviceDamageHeaderX: int = self._deviceTypeHeaderX + (len(DEVICE_TYPE_HEADER) * DEVICE_HEADER_FONT_SIZE) + TYPE_HEADER_X_GAP
        self._deviceDamageHeaderY: int = self._deviceTypeHeaderY
        self._deviceStatusHeaderX: int = self._deviceDamageHeaderX + (len(DAMAGE_HEADER) * DEVICE_HEADER_FONT_SIZE) + STATUS_HEADER_X_GAP
        self._deviceStatusHeaderY: int = self._deviceTypeHeaderY

        self._lineStartX: int = self.left + LINE_MARGIN_LEFT
        self._lineStartY: int = self.bottom + self.height - TOP_LINE_TOP_OFFSET
        self._lineEndX:   int = self.left + self.width - LINE_MARGIN_RIGHT
        self._lineEndY:   int = self._lineStartY

    def on_draw(self):
        start_render()

        self._drawHeader()
        self._drawDevicesStatus()

        self.drawDebug()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Check if any button is pressed;  Go back to the main game
        """
        self.logger.warning(f'{self.ec_top=} {self.ec_right=} {self.ec_left=} {self.ec_bottom=}')
        self.enabled = False

    def _drawHeader(self):

        deviceTypeHeaderX: int = self._deviceTypeHeaderX
        deviceTypeHeaderY: int = self._deviceTypeHeaderY

        deviceDamageHeaderX: int = self._deviceDamageHeaderX
        deviceDamageHeaderY: int = self._deviceDamageHeaderY

        deviceStatusHeaderX: int = self._deviceStatusHeaderX
        deviceStatusHeaderY: int = self._deviceStatusHeaderY

        draw_text(DEVICE_TYPE_HEADER, deviceTypeHeaderX,   deviceTypeHeaderY,   DEVICE_HEADER_COLOR, DEVICE_HEADER_FONT_SIZE)
        draw_text(DAMAGE_HEADER,      deviceDamageHeaderX, deviceDamageHeaderY, DEVICE_HEADER_COLOR, DEVICE_HEADER_FONT_SIZE)
        draw_text(STATUS_HEADER,      deviceStatusHeaderX, deviceStatusHeaderY, DEVICE_HEADER_COLOR, DEVICE_HEADER_FONT_SIZE)

        lineStartX: int = self._lineStartX
        lineStartY: int = self._lineStartY
        lineEndX:   int = self._lineEndX
        lineEndY:   int = self._lineEndY

        draw_line(start_x=lineStartX, start_y=lineStartY, end_x=lineEndX, end_y=lineEndY, color=WHITE, line_width=2)

    def _drawDevicesStatus(self):

        y: float = self._lineStartY

        for deviceType in DeviceType:
            y -= DEVICE_STATUS_LINE_GAP
            device:       Device       = self._devices.getDevice(deviceType=deviceType)
            damage:       float        = device.damage
            deviceStatus: DeviceStatus = device.deviceStatus

            draw_text(f' {deviceType}',   self._deviceTypeHeaderX,   y, DEVICE_DETAIL_COLOR, DEVICE_DETAIL_FONT_SIZE)
            draw_text(f' {damage:.2f}',   self._deviceDamageHeaderX, y, DEVICE_DETAIL_COLOR, DEVICE_DETAIL_FONT_SIZE)

            if deviceStatus == DeviceStatus.Up:
                statusColor: ColorType = STATUS_NORMAL_COLOR
            elif deviceStatus == DeviceStatus.Damaged:
                statusColor = STATUS_DAMAGED_COLOR
            elif deviceStatus == DeviceStatus.Down:
                statusColor = STATUS_DOWN_COLOR
            else:
                assert False, f'Unknown device status {deviceStatus}'

            draw_text(f' {deviceStatus}', self._deviceStatusHeaderX, y, statusColor, DEVICE_DETAIL_FONT_SIZE)

        footerY: float = y - FOOTER_GAP
        draw_line(start_x=self._lineStartX, end_x=self._lineEndX, start_y=footerY, end_y=footerY, color=WHITE, line_width=2)

    def _yRelativeToTop(self, topPosition: int):

        return self.window.height - topPosition
