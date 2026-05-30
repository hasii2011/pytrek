
from logging import Logger
from logging import getLogger

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType
from pytrek.gui.gamepieces.commander.Commander import Commander

from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator


class CommanderMediator(BaseEnemyMediator):
    """
    Handles movement updates, tactical evasions, and sound effect triggers
    specifically for Klingon Commander enemy ships.

    This mediator:
    - Periodically triggers Klingon Commander ship relocation within the current quadrant.
    - Delegates path validation and obstacle checking logic to its base enemy mediator class.
    - Triggers the unique Commander movement sound when the ship repositions.
    """

    def __init__(self):

        super().__init__()

        self.logger:        Logger       = getLogger(__name__)
        self._soundMachine: SoundMachine = SoundMachine()

    def update(self, quadrant: Quadrant, commander: Commander):
        self.moveEnemy(quadrant=quadrant, enemy=commander)

    def _playMoveSound(self):
        """
        Override super class
        """
        self._soundMachine.playSound(SoundType.CommanderMove)
