
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import load_texture

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import BaseTorpedoExplosion
from pytrek.gui.gamepieces.base.BaseAnimator import TextureList

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemy

from pytrek.gui.gamepieces.klingon.KlingonTorpedo import KlingonTorpedo
from pytrek.gui.gamepieces.klingon.KlingonTorpedoExplosion import KlingonTorpedoExplosion
from pytrek.gui.gamepieces.klingon.KlingonTorpedoExplosionColor import KlingonTorpedoExplosionColor
from pytrek.gui.gamepieces.klingon.KlingonTorpedoMiss import KlingonTorpedoMiss

from pytrek.mediators.base.MissesMediator import Misses
from pytrek.mediators.base.BaseTorpedoMediator import BaseTorpedoMediator

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType

from pytrek.LocateResources import LocateResources

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.model.Quadrant import Quadrant

from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds


class KlingonTorpedoMediator(BaseTorpedoMediator):

    def __init__(self):

        self.logger:        Logger       = getLogger(__name__)
        self._soundMachine: SoundMachine = SoundMachine()
        super().__init__()

        self._explosionTextures: TextureList = self._loadTorpedoExplosionTextures()

    @property
    def torpedoExplosionTextures(self) -> TextureList:
        return self._explosionTextures

    def draw(self):

        self.torpedoes.draw()
        self.torpedoFollowers.draw()
        self.torpedoDuds.draw()
        self.torpedoExplosions.draw()

    def update(self, quadrant: Quadrant):

        self._fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant, enemies=quadrant.klingons)
        self.torpedoes.update()
        self.torpedoFollowers.update()
        self.torpedoExplosions.update()

        self._handleTorpedoHits(quadrant, enemies=quadrant.klingons)
        self._handleTorpedoMisses(quadrant, enemies=quadrant.klingons)
        self._handleMissRemoval(quadrant, cast(Misses, self._misses))

    def _playCannotFireSound(self):
        """
        Implement empty base class method
        """
        self._soundMachine.playSound(SoundType.KlingonCannotFire)

    def _playTorpedoFiredSound(self):
        """
        Implement empty base class method
        """
        self._soundMachine.playSound(SoundType.KlingonTorpedo)

    def _playTorpedoExplodedSound(self):
        """
        We must implement this
        """
        pass

    def _loadTorpedoExplosionTextures(self) -> TextureList:

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

        speeds: TorpedoSpeeds = self._intelligence.getTorpedoSpeeds(playerType=self._gameState.playerType)

        klingonTorpedo: KlingonTorpedo = KlingonTorpedo(speed=speeds.klingon)

        klingonTorpedo.center_x = klingonPoint.x
        klingonTorpedo.center_y = klingonPoint.y
        klingonTorpedo.inMotion = True
        klingonTorpedo.destinationPoint = enterprisePoint
        klingonTorpedo.firedFromPosition = enemy.gameCoordinates
        klingonTorpedo.firedBy = enemy.id
        klingonTorpedo.followers = self.torpedoFollowers

        return klingonTorpedo

    def _getTorpedoExplosion(self) -> BaseTorpedoExplosion:
        """
        Must be implemented by subclass to create correct type of torpedo explosion

        Returns: An explosion of the correct type

        """
        return KlingonTorpedoExplosion(textureList=self._explosionTextures)

    def _getTorpedoMiss(self) -> BaseMiss:
        """
        Implement empty base class method

        Returns:  An appropriate 'miss' sprite
        """
        return KlingonTorpedoMiss(placedTime=self._gameEngine.gameClock)
