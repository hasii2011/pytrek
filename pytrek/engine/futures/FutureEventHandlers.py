
from logging import Logger
from logging import getLogger
from typing import cast

from pytrek.GameState import GameState
from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.model.Quadrant import Quadrant


class FutureEventHandlers:
    """

    """
    def __init__(self):

        self.logger:     Logger = getLogger(__name__)
        self._gameState: GameState = GameState()

    def superNovaEventHandler(self, **kwargs):
        """
        Destroy
            * Klingons
            * Planets
            * Bases
            * Mark quadrant as having been destroyed
            * Check all enemies dead
        """
        self.logger.info(f'SuperNova handler fired but am doing partial updates')
        quadrant: Quadrant = self._unPackSuperNovaArgs(**kwargs)

        self._decrementEnemyCount(quadrant=quadrant, enemyName='Klingon')
        self._decrementEnemyCount(quadrant=quadrant, enemyName='Commander')
        self._decrementEnemyCount(quadrant=quadrant, enemyName='SuperCommander')

    def tractorBeamEventHandler(self, **kwargs):
        self.logger.warning(f'TractorBeam fired but am doing Nada')

    def commanderAttacksBaseEventHandler(self, **kwargs):
        self.logger.warning(f'CommanderAttacksBase fired but am doing Nada')

    def _unPackSuperNovaArgs(self, **kwargs) -> Quadrant:

        if 'quadrant' in kwargs:
            quadrant: Quadrant = kwargs['quadrant']
            self.logger.info(f'{quadrant}')

            return quadrant

        return cast(Quadrant, None)

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
            setattr(self._gameState, gsPropertyName, remainingEnemyCount)
