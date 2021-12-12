
from logging import Logger
from logging import getLogger

from pytrek.GameState import GameState
from pytrek.engine.futures.FutureEvent import FutureEvent
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

        self._messageConsole.displayMessage(f'Message from Starfleet Command    Stardate {futureEvent.starDate:.2f}')
        self._messageConsole.displayMessage(f'Supernova in {quadrant.coordinates}; caution advised.')

        self._decrementEnemyCount(quadrant=quadrant, enemyName='Klingon')
        self._decrementEnemyCount(quadrant=quadrant, enemyName='Commander')
        self._decrementEnemyCount(quadrant=quadrant, enemyName='SuperCommander')

        if quadrant.hasStarBase is True:
            self._gameState.starBaseCount -= 1
            if self._gameState.starBaseCount < 0:
                self._gameState.starBaseCount = 0
            self._messageConsole.displayMessage(f'Starbase in quadrant {quadrant.coordinates} destroyed')

        if quadrant.hasPlanet is True:
            self._gameState.planetCount -= 1
            if self._gameState.planetCount < 0:
                self._gameState.planetCount = 0
            self._messageConsole.displayMessage(f'Planet in quadrant {quadrant.coordinates} destroyed')
        quadrant.hasSuperNova = True

    def tractorBeamEventHandler(self, futureEvent: FutureEvent):
        self._messageConsole.displayMessage(f'Tractor Beam Stardate {futureEvent.starDate:.2f}')

    def commanderAttacksBaseEventHandler(self, futureEvent: FutureEvent):
        self._messageConsole.displayMessage(f'Tractor Beam Stardate {futureEvent.starDate:.2f}')

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
        enemyCount: int = len(enemies)
        if enemyCount > 1:
            message: str = f'{len(enemies)} {enemyName}s destroyed'
        else:
            message = f'{len(enemies)} {enemyName} destroyed'

        if enemyCount > 0:
            self.logger.debug(f'{message}')
            self._messageConsole.displayMessage(message)

        for enemy in enemies:
            quadrant.decrementEnemyCount(enemy)
            remainingEnemyCount: int = getattr(self._gameState, gsPropertyName)
            remainingEnemyCount -= 1
            setattr(self._gameState, gsPropertyName, remainingEnemyCount)
