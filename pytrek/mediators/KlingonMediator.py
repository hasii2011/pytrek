
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.PlayerType import PlayerType

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.Klingon import Klingon

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
            pass    # TODO Klingons move
            # self._enemyMovedUpdateQuadrant(enemy=klingon, newPosition=, oldPosition=, quadrant=quadrant)
        else:

            arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(klingon.gameCoordinates)

            klingon.center_x = arcadePoint.x
            klingon.center_y = arcadePoint.y

    def _loadSounds(self):
        pass
