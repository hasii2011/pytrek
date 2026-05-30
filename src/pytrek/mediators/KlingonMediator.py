
from logging import Logger
from logging import getLogger

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType
from pytrek.gui.gamepieces.klingon.Klingon import Klingon

from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator


class KlingonMediator(BaseEnemyMediator):
    """
    Handles movement updates, tactical evasions, and sound effect triggers
    for  Klingon enemy ships.

    This mediator:
    - Periodically triggers Klingon ship movement within the current quadrant.
    - It delegates path validations and collision checks to its base enemy mediator class.
    - It triggers a Klingon movement sound when the ship repositions.
    """

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
