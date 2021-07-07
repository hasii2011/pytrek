
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.gui.gamepieces.commander.Commander import Commander

from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator


class CommanderMediator(BaseEnemyMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._commanderMove: Sound = cast(Sound, None)

        self._loadSounds()

    def update(self, quadrant: Quadrant, commander: Commander):
        self.moveEnemy(quadrant=quadrant, enemy=commander)

    def _playMoveSound(self):
        """
        Override super class
        """
        self._commanderMove.play(self._gameSettings.soundVolume.value)

    def _loadSounds(self):

        self._commanderMove = self._loadSound(bareFileName='CommanderMove.wav')
