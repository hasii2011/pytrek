
from logging import Logger
from logging import getLogger

from pytrek.GameState import GameState
from pytrek.engine.futures.FutureEvent import FutureEvent
from pytrek.engine.futures.FutureEventType import FutureEventType
from pytrek.gui.AbstractMessageConsole import AbstractMessageConsole

from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.model.Galaxy import Galaxy

from pytrek.model.Quadrant import Quadrant


class FutureEventHandlers:
    """

    """
    def __init__(self, messageConsole: AbstractMessageConsole):

        self.logger:          Logger    = getLogger(__name__)
        self._gameState:      GameState = GameState()
        self._galaxy:         Galaxy    = Galaxy()
        self._messageConsole: AbstractMessageConsole = messageConsole

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
        self._messageConsole.displayMessage(f'Supernova in {quadrant.coordinates}; caution advised.')

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

        else:
            from pytrek.engine.futures.EventEngine import EventEngine

            self.logger.info(f'All commanders are dead.')
            eventEngine: EventEngine = EventEngine()
            eventEngine.unScheduleEvent(FutureEventType.TRACTOR_BEAM)
            eventEngine.makeUnSchedulable(FutureEventType.TRACTOR_BEAM)

    def commanderAttacksBaseEventHandler(self, futureEvent: FutureEvent):

        if self._canCommanderAttackAStarBase() is True:
            self._standardAnnouncement(futureEvent.starDate)
            self._messageConsole.displayMessage(f'Commander attacking StarBase in {futureEvent.quadrantCoordinates}')
        else:
            from pytrek.engine.futures.EventEngine import EventEngine

            self.logger.info(f'Out of StarBases or all commanders are dead.  So no attacking StarBases')
            eventEngine: EventEngine = EventEngine()
            eventEngine.unScheduleEvent(FutureEventType.COMMANDER_ATTACKS_BASE)
            eventEngine.makeUnSchedulable(FutureEventType.COMMANDER_ATTACKS_BASE)

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
        self._messageConsole.displayMessage(f'Message from Starfleet Command    Stardate {starDate:.2f}')
