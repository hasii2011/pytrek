
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import load_texture

from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList

from pytrek.gui.gamepieces.klingon.KlingonTorpedo import KlingonTorpedo
from pytrek.gui.gamepieces.klingon.KlingonTorpedoExplosionColor import KlingonTorpedoExplosionColor
from pytrek.gui.gamepieces.klingon.KlingonTorpedoMiss import KlingonTorpedoMiss

from pytrek.mediators.base.BaseMediator import Misses
from pytrek.mediators.base.BaseTorpedoMediator import BaseTorpedoMediator

from pytrek.model.Quadrant import Quadrant
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds


class KlingonTorpedoMediator(BaseTorpedoMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__()

        self._soundKlingonTorpedo:    Sound = cast(Sound, None)
        self._soundKlingonCannotFire: Sound = cast(Sound, None)

        self._explosionTextures: TextureList = self._loadTorpedoExplosions()

        self._loadSounds()

    @property
    def torpedoExplosionTextures(self) -> TextureList:
        return self._explosionTextures

    def draw(self):

        self.torpedoes.draw()
        self.torpedoFollowers.draw()
        self.torpedoDuds.draw()

    def update(self, quadrant: Quadrant):

        self._fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant, enemies=quadrant.klingons)
        self.torpedoes.update()
        self.torpedoFollowers.update()

        self._handleTorpedoHits(quadrant, enemies=quadrant.klingons)
        self._handleTorpedoMisses(quadrant, enemies=quadrant.klingons)
        self._handleMissRemoval(quadrant, cast(Misses, self._misses))

    def _playCannotFireSound(self):
        """
        Implement empty base class method
        """
        self._soundKlingonCannotFire.play(volume=self._gameSettings.soundVolume.value)

    def _playTorpedoFiredSound(self):
        """
        Implement empty base class method
        """
        self._soundKlingonTorpedo.play(volume=self._gameSettings.soundVolume.value)

    def _playTorpedoExplodedSound(self):
        """
        We must implement this
        """
        pass

    def _loadSounds(self):

        self._soundKlingonTorpedo    = self._loadSound(bareFileName='klingonTorpedo.wav')
        # self._soundShieldHit         = self._loadSound(bareFileName='ShieldHit.wav')
        self._soundKlingonCannotFire = self._loadSound(bareFileName='KlingonCannotFire.wav')

    def _loadTorpedoExplosions(self) -> TextureList:

        textureList: TextureList = TextureList([])

        for explosionColor in KlingonTorpedoExplosionColor:

            bareFileName: str = f'KlingonTorpedoExplosion{explosionColor.value}.png'
            fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

            texture = load_texture(fqFileName)

            textureList.append(texture)

        return textureList

    def _getTorpedoToFire(self, enemy: Enemy, enterprise: Enterprise) -> BaseEnemyTorpedo:
        """

        Args:
            enemy:      The Klingon, Commander, or Super Commander that is firing
            enterprise: Where Captain Kirk is waiting

        Returns:  A torpedo of the correct kind
        """
        #
        # Use the enterprise arcade position rather than compute the sector center;  That way we
        # can use Arcade collision detection
        #
        klingonPoint:    ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)
        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)

        speeds: TorpedoSpeeds = self._intelligence.getTorpedoSpeeds()

        klingonTorpedo: KlingonTorpedo = KlingonTorpedo(speed=speeds.klingon)

        klingonTorpedo.center_x = klingonPoint.x
        klingonTorpedo.center_y = klingonPoint.y
        klingonTorpedo.inMotion = True
        klingonTorpedo.destinationPoint = enterprisePoint
        klingonTorpedo.firedFromPosition = enemy.gameCoordinates
        klingonTorpedo.firedBy = enemy.id
        klingonTorpedo.followers = self.torpedoFollowers

        return klingonTorpedo

    def _getTorpedoMiss(self) -> BaseMiss:
        """
        Implement empty base class method

        Returns:  An appropriate 'miss' sprite
        """
        return KlingonTorpedoMiss(placedTime=self._gameEngine.gameClock)
