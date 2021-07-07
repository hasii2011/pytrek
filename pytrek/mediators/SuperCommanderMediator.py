
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander

from pytrek.mediators.base.BaseEnemyMediator import BaseEnemyMediator

from pytrek.model.Quadrant import Quadrant


class SuperCommanderMediator(BaseEnemyMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._superCommanderMove: Sound = cast(Sound, None)

        self._loadSounds()

    def update(self, quadrant: Quadrant, superCommander: SuperCommander):
        self.moveEnemy(quadrant=quadrant, enemy=superCommander)

    def _playMoveSound(self):
        """
        Override super class
        """
        self._superCommanderMove.play(self._gameSettings.soundVolume.value)

    def _loadSounds(self):
        self._superCommanderMove = self._loadSound(bareFileName='SuperCommanderMove.wav')
