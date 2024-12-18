
from typing import cast
from typing import Dict
from typing import NewType

from logging import getLogger
from logging import Logger

from arcade import schedule as arcadeSchedule

from codeallybasic.SingletonV3 import SingletonV3

from pytrek.engine.Intelligence import Intelligence

from pytrek.engine.devices.DeviceManager import DeviceManager

from pytrek.engine.futures.EventCreator import EventCreator
from pytrek.engine.futures.FutureEvent import EventCallback
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.GameState import GameState

from pytrek.gui.MessageConsoleProxy import MessageConsoleProxy

from pytrek.model.Coordinates import Coordinates

from pytrek.settings.GameSettings import GameSettings

EventMap = NewType('EventMap', Dict[FutureEventType, FutureEvent])


class EventEngine(metaclass=SingletonV3):
    """
    This event engine is tied to the arcade schedule and unschedule methods
    """

    NONZERO_OPERATION_TIME_THRESHOLD: float = 0.0001
    EVENT_CHECK_INTERVAL:             float = 5.0
    """
    This constant is the amount of time that a game operation (e.g. firing, movement) must take to trigger
    a check for events. It exists so the check for zero does not have to be exact.
    
    """
    def __init__(self, *args):
        """

        Args:
            *args:  Arg 0 is the message console

        Returns:
        """

        self.logger: Logger = getLogger(__name__)

        self._intelligence: Intelligence  = Intelligence()
        self._gameState:    GameState     = GameState()
        self._gameSettings: GameSettings  = GameSettings()
        self._devices:      DeviceManager = DeviceManager()

        self._eventMap:     EventMap = cast(EventMap, None)
        self._setupEventMap()

        self._messageConsole: MessageConsoleProxy = args[0]
        self._eventCreator:   EventCreator        = EventCreator(self._messageConsole)

        self.logger.debug(f"{self._gameState.remainingGameTime=} eventMap: {self.__repr__()}")

        # TODO Put in debug option that allows selectively scheduling these
        self._scheduleRecurringEvents(eventType=FutureEventType.COMMANDER_ATTACKS_BASE)
        self._scheduleRecurringEvents(eventType=FutureEventType.TRACTOR_BEAM)
        self._scheduleRecurringEvents(eventType=FutureEventType.SUPER_NOVA)

        # I do not know what a Number is; Tell mypy so
        arcadeSchedule(function_pointer=self._doEventChecking, interval=EventEngine.EVENT_CHECK_INTERVAL)  # type: ignore

    def getEvent(self, eventType: FutureEventType) -> FutureEvent:
        return self._eventMap[eventType]

    def scheduleEvent(self, futureEvent: FutureEvent):

        eventType: FutureEventType = futureEvent.type

        futureEvent = self._debugTurnOffEvent(futureEvent=futureEvent)
        self._eventMap[eventType] = futureEvent

    def unScheduleEvent(self, eventType: FutureEventType):
        #
        # Is it already unscheduled?
        #
        futureEvent: FutureEvent = self._eventMap[eventType]
        if futureEvent.schedulable is True:

            futureEvent.type                = eventType
            futureEvent.quadrantCoordinates = cast(Coordinates, None)
            futureEvent.starDate            = 0
            futureEvent.callback            = cast(EventCallback, None)

            self._eventMap[eventType] = futureEvent

    def makeUnSchedulable(self, eventType: FutureEventType):

        futureEvent: FutureEvent = self._eventMap[eventType]

        futureEvent.schedulable = False

        self._eventMap[eventType] = futureEvent

    def debugFireEvent(self, eventType: FutureEventType):
        """
        This is a debug entry point.

        The following is for debugging events;  Requires that the debugEvents key
        in GameSettings (pytrek.ini) be set to 'True'

        Args:
            eventType:
        """
        eventToFire: FutureEvent = self.getEvent(eventType=eventType)
        self._fireEvent(eventToFire=eventToFire)

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
        Check to see if any events need to fire

        Args:
            currentStarDate:  The current star date;

        """
        for fsEventType in FutureEventType:
            if fsEventType != FutureEventType.SPY:

                futureEvent: FutureEvent = self._eventMap[fsEventType]
                # Might be unscheduled
                if futureEvent.schedulable is False:
                    pass
                else:
                    eventStartDate: float = futureEvent.starDate
                    if eventStartDate != 0 and currentStarDate >= eventStartDate:
                        self._fireEvent(eventToFire=futureEvent)
                        self._scheduleRecurringEvents(eventType=futureEvent.type)

    def _fireEvent(self, eventToFire: FutureEvent):

        self.logger.info(f'{eventToFire=}')
        if eventToFire.callback is not None:
            eventToFire.callback(eventToFire)

    def _scheduleRecurringEvents(self, eventType: FutureEventType):
        """

        Args:
            eventType:
        """
        if self._isSchedulable(eventType):

            match eventType:
                case FutureEventType.COMMANDER_ATTACKS_BASE:
                    newEvent: FutureEvent = self._eventCreator.createCommanderAttacksBaseEvent()
                    self.scheduleEvent(newEvent)
                case FutureEventType.SUPER_NOVA:
                    superNovaEvent: FutureEvent = self._eventCreator.createSuperNovaEvent()
                    self.scheduleEvent(superNovaEvent)
                case FutureEventType.TRACTOR_BEAM:
                    tractorBeamEvent: FutureEvent = self._eventCreator.createTractorBeamEvent()
                    self.scheduleEvent(tractorBeamEvent)
                case _:
                    self.logger.warning(f'Unhandled event: {eventType}')

    def _setupEventMap(self):

        eventMap: EventMap = EventMap({})

        for fsEventType in FutureEventType:
            if fsEventType != FutureEventType.SPY:
                eventMap[fsEventType] = FutureEvent(fsEventType)

        self._eventMap = eventMap

    def _isSchedulable(self, eventType: FutureEventType) -> bool:

        ans: bool = self._eventMap[eventType].schedulable
        return ans

    def _debugTurnOffEvent(self, futureEvent: FutureEvent) -> FutureEvent:
        """
        Set the appropriate flag to False to avoid scheduling certain events.  In normal mode (True)
        we schedule events

        Args:
            futureEvent:  The current event

        Returns:  Updated event set to schedulable = False

        """
        if futureEvent.type == FutureEventType.SUPER_NOVA and self._gameSettings.scheduleSuperNova is False:
            futureEvent.starDate = 0.0
            futureEvent.quadrantCoordinates = cast(Coordinates, None)
            futureEvent.schedulable = False

        if futureEvent.type == FutureEventType.COMMANDER_ATTACKS_BASE and self._gameSettings.scheduleCommanderAttacksBase is False:
            futureEvent.starDate = 0.0
            futureEvent.quadrantCoordinates = cast(Coordinates, None)
            futureEvent.schedulable = False

        if futureEvent.type == FutureEventType.TRACTOR_BEAM and self._gameSettings.scheduleTractorBeam is False:
            futureEvent.starDate = 0.0
            futureEvent.quadrantCoordinates = cast(Coordinates, None)
            futureEvent.schedulable = False

        return futureEvent

    def __repr__(self):

        myRep = "\n"
        for dictKey, fsEvent in self._eventMap.items():
            devRep = (
                f"fsEvent: {fsEvent}\n"
            )
            myRep += devRep
        return myRep
