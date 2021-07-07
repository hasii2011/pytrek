
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.gui.gamepieces.klingon.Klingon import Klingon

from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator


class KlingonMediator(BaseEnemyMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._klingonMove: Sound = cast(Sound, None)
        self._loadSounds()

    def update(self, quadrant: Quadrant, klingon: Klingon):
        self.moveEnemy(quadrant=quadrant, enemy=klingon)

    def _playMoveSound(self):
        """
        Override super class
        """
        self._klingonMove.play(self._gameSettings.soundVolume.value)

    def _loadSounds(self):

        self._klingonMove = self._loadSound('KlingonMove.wav')
