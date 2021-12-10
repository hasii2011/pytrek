
from typing import Dict
from typing import NewType

from logging import getLogger
from logging import Logger
from typing import cast

from arcade import schedule

from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.devices.Device import Device
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.futures.EventCreator import EventCreator
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.GameState import GameState

from pytrek.Singleton import Singleton
from pytrek.gui.MessageConsole import MessageConsole

EventMap = NewType('EventMap', Dict[FutureEventType, FutureEvent])


class EventEngine(Singleton):
    """
    This event engine is tied to the arcade schedule and unschedule methods
    """

    NONZERO_OPERATION_TIME_THRESHOLD: float = 0.0001
    EVENT_CHECK_INTERVAL:             float = 5.0
    """
    This constant is the amount of time that a game operation (e.g. firing, movement) must take to trigger
    a check for events. It exists so the check for zero does not have to be exact.
    
    """
    def init(self, *args, **kwargs):

        self.logger: Logger = getLogger(__name__)

        self._intelligence: Intelligence = Intelligence()
        self._gameState:    GameState    = GameState()
        self._devices:      Devices      = Devices()

        self._eventMap:     EventMap = cast(EventMap, None)
        self._setupEventMap()
        self._eventCreator: EventCreator = EventCreator()

        self._messageConsole: MessageConsole = MessageConsole()

        self.logger.debug(f"{self._gameState.inTime=} eventMap: {self.__repr__()}")

        # I do not know what a Number is tell mypy so
        schedule(function_pointer=self._doEventChecking, interval=EventEngine.EVENT_CHECK_INTERVAL)  # type: ignore

    def getEvent(self, eventType: FutureEventType) -> FutureEvent:
        return self._eventMap[eventType]

    def scheduleEvent(self, futureEvent: FutureEvent):

        eventType: FutureEventType = futureEvent.type

        self._eventMap[eventType] = futureEvent

    def unScheduleEvent(self, eventType: FutureEventType):
        self._eventMap[eventType] = cast(FutureEvent, None)

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
        self.logger.debug(f"Attempting to repair devices")
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
        """
        This is the periodic method that periodically fires
        Args:
            deltaTime:
        """

        self.logger.debug(f'{deltaTime:0.3f}')

        currentStarDate: float = self._gameState.starDate
        self.logger.info(f'Event engine running - currentStarDate: {currentStarDate:0.3f}')
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
                # Might be unscheduled
                if futureEvent is None:
                    break
                eventStarDate: float = futureEvent.starDate
                if eventStarDate != 0 and currentStarDate >= eventStarDate:
                    if fsEventType == FutureEventType.COMMANDER_ATTACKS_BASE:
                        if self._canCommanderAttackAStarBase() is False:
                            self.unScheduleEvent(FutureEventType.COMMANDER_ATTACKS_BASE)
                            break
                    self._fireEvent(eventToFire=futureEvent)
                    self._reScheduleRecurringEvents(eventType=futureEvent.type)

    def _fireEvent(self, eventToFire: FutureEvent):

        self.logger.info(f'{eventToFire=}')
        if eventToFire.callback is not None:
            eventToFire.callback(eventToFire)

    def _reScheduleRecurringEvents(self, eventType: FutureEventType):
        """
        TODO:  Use switch statement when we upgrade to 3.10

        Args:
            eventType:
        """
        if eventType == FutureEventType.COMMANDER_ATTACKS_BASE:
            newEvent: FutureEvent = self._eventCreator.createCommanderAttacksBaseEvent()
            self.scheduleEvent(newEvent)
        if eventType == FutureEventType.SUPER_NOVA:
            superNovaEvent: FutureEvent = self._eventCreator.createSuperNovaEvent()
            self.scheduleEvent(superNovaEvent)
        if eventType == FutureEventType.TRACTOR_BEAM:
            tractorBeamEvent: FutureEvent = self._eventCreator.createTractorBeamEvent()
            self.scheduleEvent(tractorBeamEvent)

    def _setupEventMap(self):

        eventMap: EventMap = EventMap({})

        for fsEventType in FutureEventType:
            if fsEventType != FutureEventType.SPY:
                eventMap[fsEventType] = FutureEvent(fsEventType)

        self._eventMap = eventMap

    def _canCommanderAttackAStarBase(self) -> bool:
        """
        There should be a commander and a star base

        Returns:  `True` if above is true, else `False`

        """
        if self._gameState.remainingCommanders == 0 or self._gameState.starBaseCount == 0:
            return False
        else:
            return True

    def __repr__(self):

        myRep = "\n"
        for dictKey, fsEvent in self._eventMap.items():
            devRep = (
                f"fsEvent: {fsEvent}\n"
            )
            myRep += devRep
        return myRep
