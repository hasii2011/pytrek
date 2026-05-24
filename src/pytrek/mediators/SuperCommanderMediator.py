
from logging import Logger
from logging import getLogger

from src.pytrek.SoundMachine import SoundMachine
from src.pytrek.SoundMachine import SoundType
from src.pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander

from src.pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator

from src.pytrek.model.Quadrant import Quadrant


class SuperCommanderMediator(BaseEnemyMediator):

    def __init__(self):

        super().__init__()

        self.logger:        Logger       = getLogger(__name__)
        self._soundMachine: SoundMachine = SoundMachine()

    def update(self, quadrant: Quadrant, superCommander: SuperCommander):
        self.moveEnemy(quadrant=quadrant, enemy=superCommander)

    def _playMoveSound(self):
        """
        Override super class
        """
        self._soundMachine.playSound(SoundType.SuperCommanderMove)
