from logging import Logger
from logging import getLogger

from pytrek.GameState import GameState

from pytrek.engine.Intelligence import Intelligence

from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy


class EventCreator:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._intelligence: Intelligence = Intelligence()
        self._gameState:    GameState    = GameState()
        self._eventEngine:  EventEngine  = EventEngine()
        self._galaxy:       Galaxy       = Galaxy()

    def scheduleInitialEvents(self):
        self.scheduleSuperNovaEvent()
        self.scheduleCommanderAttacksBaseEvent()
        self.scheduleTractorBeamEvent()

    def scheduleSuperNovaEvent(self):
        # noinspection SpellCheckingInspection
        """
        ```java
            schedule (FSNOVA, tk.expran(0.5 * game.intime));
        ```
        """

        elapsedStarDates:    float       = self._intelligence.exponentialRandom(0.5 * self._gameState.inTime)
        eventStarDate:       float       = self._gameState.starDate + elapsedStarDates
        quadrantCoordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()

        futureEvent: FutureEvent = FutureEvent(type=FutureEventType.SUPER_NOVA, starDate=eventStarDate, quadrantCoordinates=quadrantCoordinates)
        self._eventEngine.scheduleEvent(futureEvent=futureEvent)

    def scheduleCommanderAttacksBaseEvent(self):
        # noinspection SpellCheckingInspection
        """
        ```java
        schedule(FBATTAK, tk.expran(0.3*game.intime));
        ```
        """

        elapsedStarDates: float       = self._intelligence.exponentialRandom(0.3 * self._gameState.inTime)
        eventStarDate:    float       = self._gameState.starDate + elapsedStarDates
        coordinates:      Coordinates = self._galaxy.getStarBaseCoordinates()

        futureEvent: FutureEvent = FutureEvent(type=FutureEventType.COMMANDER_ATTACKS_BASE, starDate=eventStarDate, quadrantCoordinates=coordinates)
        self._eventEngine.scheduleEvent(futureEvent=futureEvent)

    def scheduleTractorBeamEvent(self):
        # noinspection SpellCheckingInspection
        """
        ```java
        schedule(FTBEAM, tk.expran(1.5 * (game.intime / game.state.remcom)));
        ```
        """
        inTime:              float = self._gameState.inTime
        remainingCommanders: int   = self._gameState.remainingCommanders
        elapsedStarDates: float       = self._intelligence.exponentialRandom(2.5 * (inTime / remainingCommanders))
        eventStarDate:    float       = self._gameState.starDate + elapsedStarDates
        coordinates:      Coordinates = self._gameState.currentQuadrantCoordinates

        futureEvent: FutureEvent = FutureEvent(type=FutureEventType.TRACTOR_BEAM, starDate=eventStarDate, quadrantCoordinates=coordinates)
        self._eventEngine.scheduleEvent(futureEvent=futureEvent)
