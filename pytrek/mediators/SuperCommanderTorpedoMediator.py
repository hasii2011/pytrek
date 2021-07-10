
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.LocateResources import LocateResources
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss
from pytrek.mediators.base.BaseTorpedoMediator import BaseTorpedoMediator
from pytrek.model.Quadrant import Quadrant


class SuperCommanderTorpedoMediator(BaseTorpedoMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__()

        self._soundSuperCommanderTorpedo:    Sound = cast(Sound, None)
        self._soundSuperCommanderCannotFire: Sound = cast(Sound, None)

        self._loadSounds()

    def draw(self):
        """
        We must implement this
        """
        pass

    def update(self, quadrant: Quadrant):
        """
        We must implement this

        Args:
            quadrant:
        """
        pass

    def _getTorpedoToFire(self, enemy: Enemy, enterprise: Enterprise) -> BaseEnemyTorpedo:
        """
        Must be implemented by subclass to create correct type of torpedo

        Args:
            enemy:      The Klingon, Commander, or Super Commander that is firing
            enterprise: Where Captain Kirk is waiting

        Returns:  A torpedo of the correct kind
        """
        pass

    def _getTorpedoMiss(self) -> BaseMiss:
        """
        Implement empty base class method

        Returns:  An appropriate 'miss' sprite
        """
        pass

    def _playCannotFireSound(self):
        """
        We must implement this
        """
        self._soundSuperCommanderCannotFire.play(volume=self._gameSettings.soundVolume.value)

    def _playTorpedoFiredSound(self):
        """
        We must implement this
        """
        self._soundSuperCommanderTorpedo.play(volume=self._gameSettings.soundVolume.value)

    def _loadSounds(self):

        self._soundSuperCommanderTorpedo    = self._loadSound(bareFileName='SuperCommanderTorpedo.wav')
        self._soundSuperCommanderCannotFire = self._loadSound(bareFileName='SuperCommanderCannotFire.wav')