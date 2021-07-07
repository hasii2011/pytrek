
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander
from pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator
from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant


class SuperCommanderMediator(BaseEnemyMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._superCommanderMove: Sound = cast(Sound, None)

        self._loadSounds()

    def update(self, quadrant: Quadrant, superCommander: SuperCommander):

        currentTime:    float = self._gameEngine.gameClock
        deltaClockTime: float = currentTime - superCommander.timeSinceMovement
        if deltaClockTime > superCommander.moveInterval:

            oldPosition: Coordinates = superCommander.gameCoordinates
            newPosition: Coordinates = self._keepTryingToMoveUntilValid(quadrant, oldPosition)

            self.logger.info(f'SuperCommander moves from {oldPosition} to {newPosition}')
            self._enemyMovedUpdateQuadrant(quadrant=quadrant, enemy=superCommander, newSectorCoordinates=newPosition, oldSectorCoordinates=oldPosition)

            superCommander.gameCoordinates = newPosition
            self._toArcadePoint(superCommander, newPosition)
            superCommander.timeSinceMovement = currentTime

            self._superCommanderMove.play(self._gameSettings.soundVolume.value)

    def _loadSounds(self):
        self._superCommanderMove = self._loadSound(bareFileName='SuperCommanderMove.wav')

