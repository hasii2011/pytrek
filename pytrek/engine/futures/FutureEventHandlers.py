
from logging import Logger
from logging import getLogger

from pytrek.GameState import GameState

from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.Intelligence import TractorBeamComputation

from pytrek.engine.futures.FutureEvent import EventCallback
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType

from pytrek.gui.ConsoleMessageType import ConsoleMessageType
from pytrek.gui.gamepieces.GamePieceTypes import Enemies

from pytrek.gui.MessageConsoleProxy import MessageConsoleProxy

from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant


class FutureEventHandlers:
    """

    """
    def __init__(self, messageConsole: MessageConsoleProxy):

        self.logger:            Logger           = getLogger(__name__)
        self._gameState:        GameState        = GameState()
        self._galaxy:           Galaxy           = Galaxy()
        self._intelligence:     Intelligence     = Intelligence()
        self._galaxyMediator:   GalaxyMediator   = GalaxyMediator()
        self._quadrantMediator: QuadrantMediator = QuadrantMediator()

        self._messageConsole: MessageConsoleProxy = messageConsole

        self.logger.debug(f'FutureEventHandlers.__init__ - {self._gameState=}')

    def superNovaEventHandler(self, futureEvent: FutureEvent):
        """
        Destroy
            * Klingons, Commanders, SuperCommanders
            * Planets
            * Bases
            * Mark quadrant as having been destroyed
            * Check all enemies dead

        Args:
            The event that caused this invocation:
        """
        quadrant: Quadrant = self._galaxy.getQuadrant(quadrantCoordinates=futureEvent.quadrantCoordinates)

        self._standardAnnouncement(futureEvent.starDate)
        self._messageConsole.displayMessage(f'Supernova in {quadrant.coordinates}; caution advised.',
                                            messageType=ConsoleMessageType.Warning)

        self._decrementEnemyCount(quadrant=quadrant, enemyName='Klingon')
        self._decrementEnemyCount(quadrant=quadrant, enemyName='Commander')
        self._decrementEnemyCount(quadrant=quadrant, enemyName='SuperCommander')

        if quadrant.hasStarBase is True:
            self._gameState.starBaseCount -= 1
            quadrant.hasStarBase = False
            self._messageConsole.displayMessage(f'Starbase in quadrant {quadrant.coordinates} destroyed')

        if quadrant.hasPlanet is True:
            self._gameState.planetCount -= 1
            quadrant.hasPlanet = False
            self._messageConsole.displayMessage(f'Planet in quadrant {quadrant.coordinates} destroyed')
        quadrant.hasSuperNova = True

    def tractorBeamEventHandler(self, futureEvent: FutureEvent):
        if self._gameState.remainingCommanders > 0:
            self._standardAnnouncement(futureEvent.starDate)
            self._messageConsole.displayMessage(f'Commander using tractor beam')
            #
            # Pick a random commander
            #
            cmdrCoordinates: Coordinates = self._galaxy.getCommanderCoordinates()
            self._messageConsole.displayMessage(f'Enterprise yanked to quadrant: {cmdrCoordinates}', messageType=ConsoleMessageType.Warning)
            #
            # Yank the Enterprise to the commander quadrant
            #
            tractorBeamComputation: TractorBeamComputation = self._intelligence.computeTractorBeamFactors(energy=self._gameState.energy)
            self._messageConsole.displayMessage(f'Warp factor set to {tractorBeamComputation.warpFactor:.2f}',
                                                messageType=ConsoleMessageType.Warning)
            currentQuadrant: Quadrant = self._galaxy.currentQuadrant
            self._galaxyMediator.doWarp(currentCoordinates=currentQuadrant.coordinates, destinationCoordinates=cmdrCoordinates)

            cmdrQuadrant: Quadrant = self._galaxy.getQuadrant(quadrantCoordinates=cmdrCoordinates)
            self._quadrantMediator.enterQuadrant(quadrant=cmdrQuadrant, enterprise=self._gameState.enterprise)

        else:
            from pytrek.engine.futures.EventEngine import EventEngine

            self.logger.info(f'All commanders are dead.')
            eventEngine: EventEngine = EventEngine()
            eventEngine.unScheduleEvent(FutureEventType.TRACTOR_BEAM)
            eventEngine.makeUnSchedulable(FutureEventType.TRACTOR_BEAM)

    def commanderAttacksBaseEventHandler(self, currentEvent: FutureEvent):
        """
        Don't schedule another command attacks base until the destroy base event fires

        Args:
            currentEvent:  The event that just occurred
        """
        from pytrek.engine.futures.EventEngine import EventEngine

        if self._canCommanderAttackAStarBase() is True:
            self._standardAnnouncement(currentEvent.starDate)
            self._messageConsole.displayMessage(f'Commander attacking StarBase in {currentEvent.quadrantCoordinates}',
                                                messageType=ConsoleMessageType.Warning)
            newEvent: FutureEvent = FutureEvent()
            newEvent.callback            = EventCallback(self.commanderDestroysBaseEventHandler)
            newEvent.type                = FutureEventType.COMMANDER_DESTROYS_BASE
            newEvent.quadrantCoordinates = currentEvent.quadrantCoordinates
            newEvent.starDate            = self._gameState.starDate + self._intelligence.computeBaseDestroyedInterval()
            eventEngine: EventEngine = EventEngine()
            eventEngine.scheduleEvent(futureEvent=newEvent)
        else:

            self.logger.info(f'Out of StarBases or all commanders are dead.  So no attacking StarBases')
            eventEngine = EventEngine()
            eventEngine.unScheduleEvent(FutureEventType.COMMANDER_ATTACKS_BASE)
            eventEngine.makeUnSchedulable(FutureEventType.COMMANDER_ATTACKS_BASE)

    def commanderDestroysBaseEventHandler(self, futureEvent: FutureEvent):
        from pytrek.engine.futures.EventEngine import EventEngine

        self._messageConsole.displayMessage(f'Commander destroyed StarBase in {futureEvent.quadrantCoordinates}',
                                            messageType=ConsoleMessageType.Warning)

        quadrant: Quadrant = self._galaxy.getQuadrant(futureEvent.quadrantCoordinates)

        assert quadrant.hasStarBase is True, 'Whoa!!  We do not have a quadrant'

        #
        # Dispose of the starbase
        #
        quadrant.hasStarBase = False
        self._gameState.starBaseCount -= 1
        eventEngine: EventEngine = EventEngine()
        eventEngine.unScheduleEvent(FutureEventType.COMMANDER_DESTROYS_BASE)

    def _decrementEnemyCount(self, quadrant: Quadrant, enemyName: str):
        """
        Decrement the appropriate enemy count

        Args:
            quadrant:   A randomly generated quadrant
            enemyName:  The enemy name, 'Klingon', 'Commander', 'SuperCommander'

        I normally don't like to write dynamically generated codes like this.  However,
        I could not in good conscience duplicate this code three times;  I know it is
        very 'Pythonic', but very high maintenance
        """
        gsPropertyName: str = f'remaining{enemyName}s'
        qPropertyName:  str = f'{enemyName[0].lower()}{enemyName[1:]}s'

        enemies: Enemies = getattr(quadrant, qPropertyName)
        for enemy in enemies:
            quadrant.decrementEnemyCount(enemy)
            remainingEnemyCount: int = getattr(self._gameState, gsPropertyName)
            remainingEnemyCount -= 1
            assert remainingEnemyCount >= 0, f'{enemyName=}  Logic error;  Fix it !'
            setattr(self._gameState, gsPropertyName, remainingEnemyCount)

        enemyCount: int = len(enemies)
        if enemyCount > 1:
            message: str = f'{len(enemies)} {enemyName}s destroyed'
        else:
            message = f'{len(enemies)} {enemyName} destroyed'

        if enemyCount > 0:
            self.logger.debug(f'{message}')
            self._messageConsole.displayMessage(message)

    def _canCommanderAttackAStarBase(self) -> bool:
        """
        There should be a commander and a star base

        Returns:  `True` if above is true, else `False`

        """
        if self._gameState.remainingCommanders == 0 or self._gameState.starBaseCount == 0:
            return False
        else:
            return True

    def _standardAnnouncement(self, starDate: float):
        self._messageConsole.displayMessage(f'Message from Starfleet Command Stardate {starDate:.2f}')
