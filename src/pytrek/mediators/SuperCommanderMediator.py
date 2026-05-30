
from logging import Logger
from logging import getLogger

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType
from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander

from pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator

from pytrek.model.Quadrant import Quadrant


class SuperCommanderMediator(BaseEnemyMediator):
    """
    Handles movement updates, tactical evasions, and sound effect triggers
    specifically for Klingon Super Commander enemy ships.

    This mediator:
    - Periodically triggers Klingon Super Commander ship relocation within the current quadrant.
    - Delegates path validation and obstacle checking logic to the base enemy mediator class.
    - Triggers the unique Super Commander movement sound when the ship repositions.
    """
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
