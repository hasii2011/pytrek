
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss
from pytrek.gui.gamepieces.supercommander.SuperCommanderTorpedo import SuperCommanderTorpedo

from pytrek.mediators.base.BaseTorpedoMediator import BaseTorpedoMediator

from pytrek.model.Quadrant import Quadrant

from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds

from pytrek.engine.ArcadePoint import ArcadePoint


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
        self.torpedoes.draw()
        self.torpedoFollowers.draw()
        self.torpedoDuds.draw()

    def update(self, quadrant: Quadrant):
        """
        We must implement this

        Args:
            quadrant:
        """
        self._fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant, enemies=quadrant.superCommanders, rotationAngle=-90)
        self.torpedoes.update()

        self._handleTorpedoHits(quadrant, enemies=quadrant.superCommanders)
        # self._handleTorpedoMisses(quadrant, enemies=quadrant.superCommanders)
        # self._handleMissRemoval(quadrant, cast(Misses, self._misses))

    def _getTorpedoToFire(self, enemy: Enemy, enterprise: Enterprise) -> BaseEnemyTorpedo:
        """
        Must be implemented by subclass to create correct type of torpedo

        Args:
            enemy:      The Klingon, Commander, or Super Commander that is firing
            enterprise: Where Captain Kirk is waiting

        Returns:  A torpedo of the correct kind
        """
        sCommanderPoint: ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)
        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)

        speeds: TorpedoSpeeds = self._intelligence.getTorpedoSpeeds()

        sCommanderTorpedo: SuperCommanderTorpedo = SuperCommanderTorpedo(speed=speeds.superCommander)

        sCommanderTorpedo.center_x = sCommanderPoint.x
        sCommanderTorpedo.center_y = sCommanderPoint.y
        sCommanderTorpedo.inMotion = True
        sCommanderTorpedo.destinationPoint  = enterprisePoint
        sCommanderTorpedo.firedFromPosition = enemy.gameCoordinates
        sCommanderTorpedo.firedBy   = enemy.id
        sCommanderTorpedo.followers = self.torpedoFollowers

        return sCommanderTorpedo

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
