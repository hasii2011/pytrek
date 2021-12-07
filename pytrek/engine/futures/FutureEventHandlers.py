
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

        klingons: Enemies = quadrant.klingons
        for klingon in klingons:
            quadrant.decrementEnemyCount(klingon)
            self._gameState.remainingKlingons -= 1

        commanders: Enemies = quadrant.commanders
        for commander in commanders:
            quadrant.decrementEnemyCount(commander)
            self._gameState.remainingCommanders -= 1

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
