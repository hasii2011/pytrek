
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.PlayerType import PlayerType

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.model.Coordinates import Coordinates

from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.BaseEnemyMediator import BaseEnemyMediator


class KlingonMediator(BaseEnemyMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._klingonMove: Sound = cast(Sound, None)
        self._loadSounds()

    def update(self, quadrant: Quadrant, klingon: Klingon):

        playerType: PlayerType = self._gameState.playerType
        if playerType == PlayerType.Emeritus or playerType == PlayerType.Expert:

            currentTime:    float = self._gameEngine.gameClock
            deltaClockTime: float = currentTime - klingon.timeSinceMovement
            if deltaClockTime > klingon.moveInterval:

                oldPosition: Coordinates = klingon.gameCoordinates
                newPosition: Coordinates = self._evade(currentLocation=oldPosition)
                self._enemyMovedUpdateQuadrant(quadrant=quadrant, enemy=klingon, newSectorCoordinates=newPosition, oldSectorCoordinates=oldPosition)

                klingon.gameCoordinates = newPosition
                self._toArcadePoint(klingon, newPosition)
                klingon.timeSinceMovement = currentTime

                # self._klingonMove.play(self._gameSettings.soundVolume.value)

        else:
            arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(klingon.gameCoordinates)

            self.logger.debug(f'{arcadePoint=}')
            # assert arcadePoint.y == 0.0, 'This sprite is off quadrant'
            klingon.center_x = arcadePoint.x
            klingon.center_y = arcadePoint.y

    def _loadSounds(self):
        pass
