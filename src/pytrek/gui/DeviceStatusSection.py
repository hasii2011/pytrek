
from logging import Logger
from logging import getLogger

from arcade import Rect
from arcade import Texture
from arcade import XYWH
from arcade import draw_texture_rect
from arcade.color import RED
from arcade.color import WHITE
from arcade.color import YELLOW

from arcade import draw_text
from arcade import draw_line
from arcade import load_texture
from arcade.types import Color

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceManager import DeviceManager

from pytrek.gui.BaseSection import BaseSection

from pytrek.LocateResources import LocateResources


EVENT_HEADER_COLOR:      Color = WHITE
DEVICE_HEADER_COLOR:     Color = WHITE
DEVICE_DETAIL_COLOR:     Color = WHITE

STATUS_NORMAL_COLOR:   Color = WHITE
STATUS_DOWN_COLOR:     Color = RED
STATUS_DAMAGED_COLOR:  Color = YELLOW

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
    BACKGROUND_WIDTH: int  = 320
    BACKGROUND_HEIGHT: int = 320

    def __init__(self, modal: bool = True, **kwargs):

        left:   int = 0
        bottom: int = SECTION_HEIGHT
        width:  int = self.window.width
        height: int = SECTION_HEIGHT

        super().__init__(left=left, bottom=bottom, width=width, height=height, modal=modal, **kwargs)

        self.logger: Logger = getLogger(__name__)

        fqFileName: str = LocateResources.getImagePath(bareFileName='MediumDarkGrayPanel.png')

        self._texture: Texture = load_texture(fqFileName)
        self._devices: DeviceManager   = DeviceManager()

        self._graphicCenterX: float = (self.top / 2) - HEADER_MARGIN_LEFT
        self._graphicCenterY: float = self.bottom + ((self.top - self.bottom) // 2)

        self._deviceTypeHeaderX:   int | float = self.left + HEADER_MARGIN_LEFT
        self._deviceTypeHeaderY:   int | float = self.bottom + self.height - TEXT_TOP_OFFSET
        self._deviceDamageHeaderX: int | float = self._deviceTypeHeaderX + (len(DEVICE_TYPE_HEADER) * DEVICE_HEADER_FONT_SIZE) + TYPE_HEADER_X_GAP
        self._deviceDamageHeaderY: int | float = self._deviceTypeHeaderY
        self._deviceStatusHeaderX: int | float = self._deviceDamageHeaderX + (len(DAMAGE_HEADER) * DEVICE_HEADER_FONT_SIZE) + STATUS_HEADER_X_GAP
        self._deviceStatusHeaderY: int | float = self._deviceTypeHeaderY

        self._lineStartX: int | float = self.left + LINE_MARGIN_LEFT
        self._lineStartY: int | float = self.bottom + self.height - TOP_LINE_TOP_OFFSET
        self._lineEndX:   int | float = self.left + self.width - LINE_MARGIN_RIGHT
        self._lineEndY:   int | float = self._lineStartY

    def on_draw(self):

        # self._texture.draw_sized(center_x=self._graphicCenterX,
        #                          center_y=self._graphicCenterY,
        #                          width=self.width + HEADER_MARGIN_LEFT,
        #                          height=self.height,
        #                          alpha=255)
        rect: Rect = XYWH(x=self._graphicCenterX,
                          y=self._graphicCenterY,
                          width=self.width + HEADER_MARGIN_LEFT,
                          height=self.height)
        draw_texture_rect(texture=self._texture,
                          rect=rect,
                          alpha=255)

        self._drawHeader()
        self._drawDevicesStatus()

        self.drawDebug()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Check if any button is pressed;  Go back to the main game
        """
        self.logger.warning(f'{self.top=} {self.right=} {self.left=} {self.bottom=}')
        self.enabled = False

    def _drawHeader(self):

        deviceTypeHeaderX: int | float = self._deviceTypeHeaderX
        deviceTypeHeaderY: int | float = self._deviceTypeHeaderY

        deviceDamageHeaderX: int | float = self._deviceDamageHeaderX
        deviceDamageHeaderY: int | float = self._deviceDamageHeaderY

        deviceStatusHeaderX: int | float = self._deviceStatusHeaderX
        deviceStatusHeaderY: int | float = self._deviceStatusHeaderY

        draw_text(DEVICE_TYPE_HEADER, deviceTypeHeaderX,   deviceTypeHeaderY,   DEVICE_HEADER_COLOR.rgb, DEVICE_HEADER_FONT_SIZE)
        draw_text(DAMAGE_HEADER,      deviceDamageHeaderX, deviceDamageHeaderY, DEVICE_HEADER_COLOR.rgb, DEVICE_HEADER_FONT_SIZE)
        draw_text(STATUS_HEADER,      deviceStatusHeaderX, deviceStatusHeaderY, DEVICE_HEADER_COLOR.rgb, DEVICE_HEADER_FONT_SIZE)

        lineStartX: int | float = self._lineStartX
        lineStartY: int | float = self._lineStartY
        lineEndX:   int | float = self._lineEndX
        lineEndY:   int | float = self._lineEndY

        draw_line(start_x=lineStartX, start_y=lineStartY, end_x=lineEndX, end_y=lineEndY, color=WHITE, line_width=2)

    def _drawDevicesStatus(self):

        y: float = self._lineStartY

        for deviceType in DeviceType:
            y -= DEVICE_STATUS_LINE_GAP
            device:       Device       = self._devices.getDevice(deviceType=deviceType)
            damage:       float        = device.damage
            deviceStatus: DeviceStatus = device.deviceStatus

            draw_text(f' {deviceType}',   self._deviceTypeHeaderX,   y, DEVICE_DETAIL_COLOR.rgb, DEVICE_DETAIL_FONT_SIZE)
            draw_text(f' {damage:.2f}',   self._deviceDamageHeaderX, y, DEVICE_DETAIL_COLOR.rgb, DEVICE_DETAIL_FONT_SIZE)

            if deviceStatus == DeviceStatus.Up:
                statusColor: Color = STATUS_NORMAL_COLOR
            elif deviceStatus == DeviceStatus.Damaged:
                statusColor = STATUS_DAMAGED_COLOR
            elif deviceStatus == DeviceStatus.Down:
                statusColor = STATUS_DOWN_COLOR
            else:
                assert False, f'Unknown device status {deviceStatus}'

            draw_text(f' {deviceStatus}', self._deviceStatusHeaderX, y, statusColor.rgb, DEVICE_DETAIL_FONT_SIZE)

        footerY: float = y - FOOTER_GAP
        draw_line(start_x=self._lineStartX, end_x=self._lineEndX, start_y=footerY, end_y=footerY, color=WHITE, line_width=2)

    def _yRelativeToTop(self, topPosition: int):

        return self.window.height - topPosition
