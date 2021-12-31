
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
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon
from tests.SchedulerTestMessageConsole import SchedulerTestMessageConsole

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

HELP_SEPARATOR_Y: int = 125
HELP_Y:           int = HELP_SEPARATOR_Y - 25
GAME_STATE_Y:     int = HELP_SEPARATOR_Y + 50


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

        self._messageConsole:   SchedulerTestMessageConsole = SchedulerTestMessageConsole()
        self._eventEngine:      EventEngine                 = EventEngine(self._messageConsole)
        self._quadrantMediator: QuadrantMediator            = QuadrantMediator()

        self._quadrant: Quadrant = self._galaxy.currentQuadrant

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        enterprise: Enterprise = self._gameState.enterprise

        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=enterprise)

        self._createInitialEvents()

    def setup(self):
        pass

    def on_draw(self):
        start_render()
        # def draw_line(start_x: float, start_y: float, end_x: float, end_y: float, color: Color, line_width: float = 1)
        self._drawHeader()
        self._drawDevicesStatus()
        self._drawEventStatus()
        self._drawGameState()
        self._drawHelpText()
        self._messageConsole.draw()

    def _drawHeader(self):
        # Header
        draw_text(f'Event Type', EVENT_TYPE_X, EVENT_TYPE_Y, EVENT_HEADER_COLOR, EVENT_HEADER_FONT_SIZE)
        # Separator line
        draw_line(start_x=EVENT_TYPE_X, end_x=SCREEN_WIDTH - (2 * X_MARGIN),
                  start_y=EVENT_TYPE_Y, end_y=EVENT_TYPE_Y,
                  color=color.WHITE, line_width=2)

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

        footerY: float = y - 5
        endX:    float = SCREEN_WIDTH - (2 * X_MARGIN)
        draw_line(start_x=DEVICE_TYPE_X, end_x=endX, start_y=footerY, end_y=footerY, color=color.WHITE, line_width=2)

    def _drawEventStatus(self):
        # The events
        y: float = EVENT_TYPE_Y - 20
        for eventType in FutureEventType:
            if eventType != FutureEventType.SPY:
                y -= 20
                event: FutureEvent = self._eventEngine.getEvent(eventType=eventType)

                draw_text(f'{event.type.value}', EVENT_TYPE_X, y, EVENT_DETAIL_COLOR, EVENT_DETAIL_FONT_SIZE)
                draw_text(f'{event.starDate:.2f}', EVENT_DATE_X, y, EVENT_DETAIL_COLOR, EVENT_DETAIL_FONT_SIZE)
                draw_text(f'{event.quadrantCoordinates}', EVENT_COORDINATES_X, y, EVENT_DETAIL_COLOR, EVENT_DETAIL_FONT_SIZE)

    def _drawGameState(self):
        starDate: float = self._gameState.starDate
        draw_text(f'Current Star Date: {starDate:.2f}', 10, GAME_STATE_Y, color.YELLOW, 12)
        draw_text(f'Klingon Count: {self._gameState.remainingKlingons}',     225, GAME_STATE_Y, color.YELLOW, 12)
        draw_text(f'Commander Count: {self._gameState.remainingCommanders}', 365, GAME_STATE_Y, color.YELLOW, 12)
        draw_text(f'StarBase Count: {self._gameState.starBaseCount}',        530, GAME_STATE_Y, color.YELLOW, 12)

    def _drawHelpText(self):
        draw_line(start_x=10, end_x=SCREEN_WIDTH - (2 * X_MARGIN), start_y=HELP_SEPARATOR_Y, end_y=HELP_SEPARATOR_Y, color=color.YELLOW, line_width=1)
        draw_text(f'Q: `Quit`   1-9: `Update Time`   C: `Kill Commanders`   A: `Reset`', 10, HELP_Y, color.YELLOW)

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
        Called whenever the user releases a previously pressed key.
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
        elif self._wasNumberPressed(releasedKey=releasedKey) is True:
            self._gameEngine.updateTime(elapsedTime=self._keyToValue(releasedKey))

    def _createInitialEvents(self):

        eventCreator: EventCreator = EventCreator(self._messageConsole)
        superNovaEvent:           FutureEvent = eventCreator.createSuperNovaEvent()
        commanderAttackBaseEvent: FutureEvent = eventCreator.createCommanderAttacksBaseEvent()
        tractorBeamEvent:         FutureEvent = eventCreator.createTractorBeamEvent()

        self._eventEngine.scheduleEvent(futureEvent=superNovaEvent)
        self._eventEngine.scheduleEvent(futureEvent=commanderAttackBaseEvent)
        self._eventEngine.scheduleEvent(futureEvent=tractorBeamEvent)

    def _wasNumberPressed(self, releasedKey: int) -> bool:
        """
        Recognizes 1-9;  incrementing the star date by 0 makes no sense
        Args:
            releasedKey:  The arcade key that was pressed

        Returns:  `True` if between 1 and 9 inclusive, else `False`
        """

        ans: bool = False
        if arcadeKey.KEY_1 <= releasedKey <= arcadeKey.KEY_9:
            ans = True
        return ans

    def _keyToValue(self, releasedKey: int):
        """
        Assumes the arcade key values are numerically ascending
        Args:
            releasedKey:  The arcade key that was pressed

        Returns: A value between 1-9
        """
        return releasedKey - arcadeKey.KEY_0


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
