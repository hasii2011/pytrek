
from logging import Logger
from logging import getLogger

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType
from pytrek.gui.gamepieces.klingon.Klingon import Klingon

from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator


class KlingonMediator(BaseEnemyMediator):

    def __init__(self):

        super().__init__()

        self.logger:        Logger       = getLogger(__name__)
        self._soundMachine: SoundMachine = SoundMachine()

    def update(self, quadrant: Quadrant, klingon: Klingon):
        self.moveEnemy(quadrant=quadrant, enemy=klingon)

    def _playMoveSound(self):
        """
        Override super class
        """
        self._soundMachine.playSound(SoundType.KlingonMove)
