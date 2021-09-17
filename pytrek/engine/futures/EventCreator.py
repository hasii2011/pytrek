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

    def createInitialEvents(self):
        self._createSuperNovaEvent()
        self._createCommanderAttacksBaseEvent()

    def _createSuperNovaEvent(self):

        elapsedStarDates:    float       = self._intelligence.exponentialRandom(0.5 * self._gameState.inTime)
        eventStarDate:       float       = self._gameState.starDate + elapsedStarDates
        quadrantCoordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()

        futureEvent: FutureEvent = FutureEvent(type=FutureEventType.SUPER_NOVA, starDate=eventStarDate, quadrantCoordinates=quadrantCoordinates)
        self._eventEngine.scheduleEvent(futureEvent=futureEvent)

    def _createCommanderAttacksBaseEvent(self):

        elapsedStarDates: float       = self._intelligence.exponentialRandom(0.3 * self._gameState.inTime)
        eventStarDate:    float       = self._gameState.starDate + elapsedStarDates
        coordinates:      Coordinates = self._galaxy.getStarBaseCoordinates()

        futureEvent: FutureEvent = FutureEvent(type=FutureEventType.COMMANDER_ATTACKS_BASE, starDate=eventStarDate, quadrantCoordinates=coordinates)
        self._eventEngine.scheduleEvent(futureEvent=futureEvent)
