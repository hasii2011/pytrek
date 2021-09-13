
from typing import Dict
from typing import NewType

from logging import getLogger
from logging import Logger

from arcade import schedule

from pytrek.GameState import GameState
from pytrek.Singleton import Singleton

from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType

EventMap = NewType('EventMap', Dict[FutureEventType, FutureEvent])


class EventEngine(Singleton):
    """
    This event engine is tied to the arcade schedule and unschedule methods
    """

    NONZERO_OPERATION_TIME_THRESHOLD: float = 0.0001
    """
    This constant is the amount of time that a game operation (e.g. firing, movement) must take to trigger
    a check for events. It exists so the check for zero does not have to be exact.
    """
    def init(self, *args, **kwargs):

        self.logger: Logger = getLogger(__name__)

        self._intelligence: Intelligence = Intelligence()
        self._gameState:    GameState    = GameState()
        self._devices:      Devices      = Devices()

        self._eventMap: EventMap = EventMap({})
        for fsEventType in FutureEventType:
            if fsEventType != FutureEventType.SPY:
                self._eventMap[fsEventType] = FutureEvent(fsEventType)

        elapsedStarDates: float = self._intelligence.exponentialRandom(0.5 * self._gameState.inTime)
        eventStarDate:    float = self._gameState.starDate + elapsedStarDates
        self._eventMap[FutureEventType.SUPER_NOVA]  = self._createFutureEvent(FutureEventType.SUPER_NOVA, eventStarDate=eventStarDate)

        elapsedStarDates = self._intelligence.exponentialRandom(0.3 * self._gameState.inTime)
        eventStarDate    = self._gameState.starDate + elapsedStarDates

        self._eventMap[FutureEventType.COMMANDER_ATTACKS_BASE] = self._createFutureEvent(FutureEventType.COMMANDER_ATTACKS_BASE, eventStarDate=eventStarDate)

        self.logger.info(f"{self._gameState.inTime=} eventMap: {self.__repr__()}")

        # I do not know what a Number is  tell mypy so
        schedule(function_pointer=self._doEventChecking, interval=5.0)  # type: ignore

    def fixDevices(self):
        # noinspection SpellCheckingInspection
        """
        // #define Time a.Time // time taken by current operation
        double fintim = d.date + Time
        datemin = fintim;

        // d.date is current stardate

        xtime = datemin-d.date;

        repair = xtime;

        /* Don't fix Deathray here */
        for (l=1; l<=ndevice; l++)
            if (damage[l] > 0.0 && l != DDRAY)
                damage[l] -= (damage[l]-repair > 0.0 ? repair : damage[l]);

        /* Fix Deathray if docked */
        if (damage[DDRAY] > 0.0 && condit == IHDOCKED)
            damage[DDRAY] -= (damage[l] - xtime > 0.0 ? xtime : damage[DDRAY]);

        /* If radio repaired, update star chart and attack reports */

        """
        self.logger.info(f"Attempting to repair devices")
        finishTime:  float = self._gameState.starDate + self._gameState.opTime
        dateMinimum: float = finishTime
        extraTime:   float = dateMinimum - self._gameState.starDate
        repair:      float = extraTime

        for devType in DeviceType:
            device: Device = self._devices.getDevice(devType)
            if device.deviceType != DeviceType.DeathRay:
                if device.damage > 0.0:
                    device.damage = device.damage - repair
                    if device.damage <= 0:
                        device.damage = 0
                        device.deviceStatus = DeviceStatus.Up
                        self.logger.info(f"Device: {device.deviceType.name} repaired")

    def _doEventChecking(self, deltaTime: float):
        self.logger.info(f'Asynchronous event engine running - {deltaTime:0.3f}')

        currentStarDate: float = self._gameState.starDate
        self._checkEvents(currentStarDate=currentStarDate)

    def _checkEvents(self, currentStarDate: float):
        """
        Check to see if any events need to fire off
        Args:
            currentStarDate:  The current star date;

        """

        for fsEventType in FutureEventType:
            if fsEventType != FutureEventType.SPY:

                futureEvent: FutureEvent = self._eventMap[fsEventType]
                eventStarDate: float = futureEvent.starDate
                if eventStarDate != 0 and eventStarDate >= currentStarDate:
                    self._fireEvent(eventToFire=futureEvent)

    def _fireEvent(self, eventToFire: FutureEvent):

        self.logger.info(f'{eventToFire=}')

    def _createFutureEvent(self, fEventType: FutureEventType, eventStarDate: float) -> FutureEvent:

        retEvent: FutureEvent = FutureEvent(type=fEventType, starDate=eventStarDate)

        return retEvent

    def __repr__(self):

        myRep = "\n"
        for dictKey, fsEvent in self._eventMap.items():
            devRep = (
                f"fsEvent: {fsEvent}\n"
            )
            myRep += devRep
        return myRep
