
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.gui.gamepieces.commander.Commander import Commander

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator


class CommanderMediator(BaseEnemyMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._commanderMove: Sound = cast(Sound, None)

        self._loadSounds()

    def update(self, quadrant: Quadrant, commander: Commander):

        currentTime:    float = self._gameEngine.gameClock
        deltaClockTime: float = currentTime - commander.timeSinceMovement
        if deltaClockTime > commander.moveInterval:

            oldPosition: Coordinates = commander.gameCoordinates
            newPosition: Coordinates = self._keepTryingToMoveUntilValid(quadrant, oldPosition)

            self.logger.info(f'Commander moves from {oldPosition} to {newPosition}')
            self._enemyMovedUpdateQuadrant(quadrant=quadrant, enemy=commander, newSectorCoordinates=newPosition, oldSectorCoordinates=oldPosition)

            commander.gameCoordinates = newPosition
            self._toArcadePoint(commander, newPosition)
            commander.timeSinceMovement = currentTime

            self._commanderMove.play(self._gameSettings.soundVolume.value)

    def _loadSounds(self):

        self._commanderMove = self._loadSound(bareFileName='CommanderMove.wav')
