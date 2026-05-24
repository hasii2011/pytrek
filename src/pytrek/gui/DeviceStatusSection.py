
from typing import cast
from typing import NewType

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from arcade import Rect
from arcade import Texture
from arcade import XYWH
from arcade import Text
from arcade import draw_line

from arcade import load_texture
from arcade import draw_texture_rect

from arcade.color import RED
from arcade.color import WHITE
from arcade.color import YELLOW

from arcade.types import Color

from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceManager import DeviceManager

from pytrek.gui.BaseSection import BaseSection

from pytrek.gui.Common import dimBackgroundForView

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


@dataclass
class DeviceTextRow:
    typeText: Text
    damageText: Text
    statusText: Text


DeviceTextRows = NewType('DeviceTextRows', dict[DeviceType, DeviceTextRow])


class DeviceStatusSection(BaseSection):
    """
    Represents a self-sizing overlay section that displays the status, damage levels, and operational
    states of the Enterprise's devices.

    Functionality:
    1. Status Board Display:
       - Renders a semi-transparent dark gray panel overlay.
       - Displays columns for Device Type, Damage, and Status, bounded by horizontal separator lines.
    2. Device Information Formatting:
       - Queries the DeviceManager for all device types.
       - Renders each device's numeric damage level formatted to two decimal places.
       - Colors the status value dynamically based on its state: white for Normal (Up), yellow for Damaged, and red for Down.
    3. Interaction:
       - Closes/dismisses the status display overlay when the user clicks anywhere in the section.
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

        self._texture: Texture       = load_texture(fqFileName)
        self._devices: DeviceManager = DeviceManager()

        self._graphicCenterX: float = (self.top / 2) - HEADER_MARGIN_LEFT
        self._graphicCenterY: float = self.bottom + ((self.top - self.bottom) // 2)

        self._deviceTypeHeaderX:   int | float = self.left + HEADER_MARGIN_LEFT
        self._deviceTypeHeaderY:   int | float = self.bottom + self.height - TEXT_TOP_OFFSET
        self._deviceDamageHeaderX: int | float = self._deviceTypeHeaderX + (len(DEVICE_TYPE_HEADER) * DEVICE_HEADER_FONT_SIZE) + TYPE_HEADER_X_GAP
        self._deviceDamageHeaderY: int | float = self._deviceTypeHeaderY
        self._deviceStatusHeaderX: int | float = self._deviceDamageHeaderX + (len(DAMAGE_HEADER) * DEVICE_HEADER_FONT_SIZE) + STATUS_HEADER_X_GAP
        self._deviceStatusHeaderY: int | float = self._deviceTypeHeaderY

        self._deviceTypeHeaderText: Text = cast(Text, None)     # noqa
        self._damageHeaderText:     Text = cast(Text, None)     # noqa
        self._statusHeaderText:     Text = cast(Text, None)     # noqa

        self._initializeDeviceHeaderRow()

        self._lineStartX: int | float = self.left + LINE_MARGIN_LEFT
        self._lineStartY: int | float = self.bottom + self.height - TOP_LINE_TOP_OFFSET
        self._lineEndX:   int | float = self.left + self.width - LINE_MARGIN_RIGHT
        self._lineEndY:   int | float = self._lineStartY

        self._deviceTextRows: DeviceTextRows = self._initializeDeviceTextRows(lineStartY=self._lineStartY)

        y: float = self._lineStartY - (len(DeviceType) * DEVICE_STATUS_LINE_GAP)
        self._footerLineY: float = y - FOOTER_GAP

    def on_draw(self):

        dimBackgroundForView(windowWidth=self.window.width, windowHeight=self.window.height)

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

        self._deviceTypeHeaderText.draw()
        self._damageHeaderText.draw()
        self._statusHeaderText.draw()

        lineStartX: int | float = self._lineStartX
        lineStartY: int | float = self._lineStartY
        lineEndX:   int | float = self._lineEndX
        lineEndY:   int | float = self._lineEndY

        draw_line(start_x=lineStartX, start_y=lineStartY, end_x=lineEndX, end_y=lineEndY, color=WHITE, line_width=2)

    def _drawDevicesStatus(self):

        for deviceType in DeviceType:
            device:       Device        = self._devices.getDevice(deviceType=deviceType)
            damage:       float = device.damage
            deviceStatus: DeviceStatus  = device.deviceStatus

            if deviceStatus == DeviceStatus.Up:
                statusColor: Color = STATUS_NORMAL_COLOR
            elif deviceStatus == DeviceStatus.Damaged:
                statusColor = STATUS_DAMAGED_COLOR
            elif deviceStatus == DeviceStatus.Down:
                statusColor = STATUS_DOWN_COLOR
            else:
                assert False, f'Unknown device status {deviceStatus}'

            textRow: DeviceTextRow = self._deviceTextRows[deviceType]
            textRow.damageText.text = f' {damage:.2f}'
            textRow.statusText.text = f' {deviceStatus}'
            textRow.statusText.color = statusColor

            textRow.typeText.draw()
            textRow.damageText.draw()
            textRow.statusText.draw()

        draw_line(start_x=self._lineStartX, end_x=self._lineEndX, start_y=self._footerLineY, end_y=self._footerLineY, color=WHITE, line_width=2)

    def _yRelativeToTop(self, topPosition: int):

        return self.window.height - topPosition

    def _initializeDeviceHeaderRow(self):
        """
        Initializes the appropriate instance variables
        """

        self._deviceTypeHeaderText = Text(
            text=DEVICE_TYPE_HEADER,
            x=self._deviceTypeHeaderX,
            y=self._deviceTypeHeaderY,
            color=DEVICE_HEADER_COLOR.rgb,
            font_size=DEVICE_HEADER_FONT_SIZE
        )
        self._damageHeaderText = Text(
            text=DAMAGE_HEADER,
            x=self._deviceDamageHeaderX,
            y=self._deviceDamageHeaderY,
            color=DEVICE_HEADER_COLOR.rgb,
            font_size=DEVICE_HEADER_FONT_SIZE
        )
        self._statusHeaderText = Text(
            text=STATUS_HEADER,
            x=self._deviceStatusHeaderX,
            y=self._deviceStatusHeaderY,
            color=DEVICE_HEADER_COLOR.rgb,
            font_size=DEVICE_HEADER_FONT_SIZE
        )

    def _initializeDeviceTextRows(self, lineStartY) -> DeviceTextRows:

        deviceTextRows: DeviceTextRows = DeviceTextRows({})
        # y:              float  = self._lineStartY
        y:              float  = lineStartY

        for deviceType in DeviceType:
            y -= DEVICE_STATUS_LINE_GAP
            typeText: Text = Text(
                text=f' {deviceType}',
                x=self._deviceTypeHeaderX,
                y=y,
                color=DEVICE_DETAIL_COLOR.rgb,
                font_size=DEVICE_DETAIL_FONT_SIZE
            )
            damageText: Text = Text(
                text='',
                x=self._deviceDamageHeaderX,
                y=y,
                color=DEVICE_DETAIL_COLOR.rgb,
                font_size=DEVICE_DETAIL_FONT_SIZE
            )
            statusText: Text = Text(
                text='',
                x=self._deviceStatusHeaderX,
                y=y,
                color=STATUS_NORMAL_COLOR.rgb,
                font_size=DEVICE_DETAIL_FONT_SIZE
            )
            deviceTextRows[deviceType] = DeviceTextRow(
                typeText=typeText,
                damageText=damageText,
                statusText=statusText
            )

        return deviceTextRows
