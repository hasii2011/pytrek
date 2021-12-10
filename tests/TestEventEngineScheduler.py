
from logging import Logger
from logging import getLogger

from arcade import View
from arcade import Window
from arcade import color
from arcade import draw_line
from arcade import draw_text

from arcade import run as arcadeRun
from arcade import key as arcadeKey
from arcade import start_render

from pytrek.GameState import GameState

from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.futures.EventCreator import EventCreator
from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase

SCREEN_WIDTH:  int = 960
SCREEN_HEIGHT: int = 600

SCREEN_TITLE: str = 'Test Event Scheduler'

DEVICE_HEADER_FONT_SIZE: int = 14
DEVICE_HEADER_COLOR:     tuple[int, int, int]  = color.WHITE
X_MARGIN:        float = 10.0
Y_MARGIN:        float = 24.0
DEVICE_Y:        float = SCREEN_HEIGHT - Y_MARGIN
DEVICE_TYPE_X:   float = X_MARGIN
DEVICE_DAMAGE_X: float = DEVICE_TYPE_X + 190
DEVICE_STATUS_X: float = DEVICE_DAMAGE_X + 100

DEVICE_DETAIL_COLOR:     tuple[int, int, int] = color.WHITE
DEVICE_DETAIL_FONT_SIZE: int = 12

EVENT_TYPE_X:           float = DEVICE_STATUS_X + 120
EVENT_DATE_X:           float = EVENT_TYPE_X    + 210
EVENT_COORDINATES_X:    float = EVENT_DATE_X + 100
EVENT_TYPE_Y:           float = DEVICE_Y

EVENT_HEADER_COLOR:     tuple[int, int, int] = color.WHITE
EVENT_HEADER_FONT_SIZE: int = 14

EVENT_DETAIL_COLOR:     tuple[int, int, int] = color.WHITE
EVENT_DETAIL_FONT_SIZE: int = 12


class TestEventScheduler(View):

    def __init__(self):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._gameSettings: GameSettings = GameSettings()
        self._gameState:    GameState    = GameState()
        self._gameEngine:   GameEngine   = GameEngine()
        self._intelligence: Intelligence = Intelligence()
        self._computer:     Computer     = Computer()
        self._galaxy:       Galaxy       = Galaxy()
        self._devices:      Devices      = Devices()
        self._eventEngine:  EventEngine  = EventEngine()

        self._quadrant: Quadrant = self._galaxy.currentQuadrant

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        self._createInitialEvents()

    def setup(self):
        pass

    def on_draw(self):
        start_render()
        # def draw_line(start_x: float, start_y: float, end_x: float, end_y: float, color: Color, line_width: float = 1)
        self._drawDevicesStatus()
        # Header
        draw_text(f'Event Type', EVENT_TYPE_X, EVENT_TYPE_Y, EVENT_HEADER_COLOR, EVENT_HEADER_FONT_SIZE)
        draw_text(f'Event Date', EVENT_DATE_X, EVENT_TYPE_Y, EVENT_HEADER_COLOR, EVENT_HEADER_FONT_SIZE)
        # Separator line
        draw_line(start_x=EVENT_TYPE_X, end_x=SCREEN_WIDTH - (2 * X_MARGIN),
                  start_y=EVENT_TYPE_Y, end_y=EVENT_TYPE_Y,
                  color=color.WHITE, line_width=2)

        # The events
        y: float = EVENT_TYPE_Y - 20
        for eventType in FutureEventType:
            if eventType != FutureEventType.SPY:
                y -= 20
                event: FutureEvent = self._eventEngine.getEvent(eventType=eventType)
                draw_text(f'{event.type.value}', EVENT_TYPE_X, y, EVENT_DETAIL_COLOR, EVENT_DETAIL_FONT_SIZE)
                draw_text(f'{event.starDate:.2f}',        EVENT_DATE_X,        y, EVENT_DETAIL_COLOR, EVENT_DETAIL_FONT_SIZE)
                draw_text(f'{event.quadrantCoordinates}', EVENT_COORDINATES_X, y, EVENT_DETAIL_COLOR, EVENT_DETAIL_FONT_SIZE)

        starDate: float = self._gameState.starDate
        draw_text(f'Current Star Date: {starDate}', 10, 100, color.GLAUCOUS, 12)
        draw_text(f'Q: `Quit` U: `Update Time` C: `Kill Commanders` A: `Reset`', 10, 50, color.GLAUCOUS)

    def _drawDevicesStatus(self):

        # Header
        draw_text(f'Device type', DEVICE_TYPE_X, DEVICE_Y, DEVICE_HEADER_COLOR, DEVICE_HEADER_FONT_SIZE)
        draw_text(f'Damage',      DEVICE_DAMAGE_X, DEVICE_Y, DEVICE_HEADER_COLOR, DEVICE_HEADER_FONT_SIZE)
        draw_text(f'Status',      DEVICE_STATUS_X, DEVICE_Y, DEVICE_HEADER_COLOR, DEVICE_HEADER_FONT_SIZE)

        # Separator line
        draw_line(start_x=DEVICE_TYPE_X, end_x=(SCREEN_WIDTH / 2) - (2 * X_MARGIN),
                  start_y=DEVICE_Y, end_y=DEVICE_Y,
                  color=color.WHITE, line_width=2)

        # Devices themselves
        y: float = DEVICE_Y - 20

        for deviceType in DeviceType:
            y -= 20
            device: Device = self._devices.getDevice(deviceType=deviceType)
            damage: float = device.damage
            deviceStatus: DeviceStatus = device.deviceStatus
            draw_text(f' {deviceType}', DEVICE_TYPE_X, y, DEVICE_DETAIL_COLOR, DEVICE_DETAIL_FONT_SIZE)
            draw_text(f' {damage:.2f}', DEVICE_DAMAGE_X, y, DEVICE_DETAIL_COLOR, DEVICE_DETAIL_FONT_SIZE)
            draw_text(f' {deviceStatus}', DEVICE_STATUS_X, y, DEVICE_DETAIL_COLOR, DEVICE_DETAIL_FONT_SIZE)

    def on_update(self, deltaTime: float):
        """
        Normal done by PyTrekView code;  We need to simulate updating the
        real time clock
        Args:
            deltaTime:

        Returns:

        """
        self._gameEngine.updateRealTimeClock(deltaTime=deltaTime)

    def on_key_release(self, releasedKey: int, key_modifiers: int):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if releasedKey == arcadeKey.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)
        elif releasedKey == arcadeKey.U:
            self._gameEngine.updateTime(elapsedTime=1.0)
        elif releasedKey == arcadeKey.A:
            self.setup()
        elif releasedKey == arcadeKey.C:
            self._gameState.remainingCommanders = 0

    def _createInitialEvents(self):

        eventCreator: EventCreator = EventCreator()
        superNovaEvent:           FutureEvent = eventCreator.createSuperNovaEvent()
        commanderAttackBaseEvent: FutureEvent = eventCreator.createCommanderAttacksBaseEvent()
        tractorBeamEvent:         FutureEvent = eventCreator.createTractorBeamEvent()

        self._eventEngine.scheduleEvent(futureEvent=superNovaEvent)
        self._eventEngine.scheduleEvent(futureEvent=commanderAttackBaseEvent)
        self._eventEngine.scheduleEvent(futureEvent=tractorBeamEvent)


def main():

    TestBase.setUpLogging()
    SettingsCommon.determineSettingsLocation()

    window:    Window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    startView: TestEventScheduler  = TestEventScheduler()

    window.show_view(startView)

    startView.setup()

    arcadeRun()


if __name__ == "__main__":
    main()
