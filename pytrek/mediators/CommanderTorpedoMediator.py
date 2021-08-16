
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import load_spritesheet


from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import BaseTorpedoExplosion
from pytrek.gui.gamepieces.base.BaseAnimator import TextureList
from pytrek.gui.gamepieces.commander.Commander import Commander

from pytrek.gui.gamepieces.commander.CommanderTorpedo import CommanderTorpedo
from pytrek.gui.gamepieces.commander.CommanderTorpedoExplosion import CommanderTorpedoExplosion
from pytrek.gui.gamepieces.commander.CommanderTorpedoMiss import CommanderTorpedoMiss

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemy

from pytrek.mediators.base.BaseMediator import BaseMediator
from pytrek.mediators.base.MissesMediator import Misses
from pytrek.mediators.base.BaseTorpedoMediator import BaseTorpedoMediator

from pytrek.model.Quadrant import Quadrant

from pytrek.LocateResources import LocateResources

from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds


class CommanderTorpedoMediator(BaseTorpedoMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__()

        self._soundCommanderTorpedo:    Sound = cast(Sound, None)
        self._soundCommanderCannotFire: Sound = cast(Sound, None)

        self._loadSounds()
        self._explosionTextures: TextureList = self._loadTorpedoExplosionTextures()

    @property
    def torpedoExplosionTextures(self) -> TextureList:
        return self._explosionTextures

    def draw(self):
        """
        We must implement this
        """
        self.torpedoes.draw()
        self.torpedoFollowers.draw()
        self.torpedoDuds.draw()
        self.torpedoExplosions.draw()

    def update(self, quadrant: Quadrant):
        """
        We must implement this

        Args:
            quadrant:
        """
        self._fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant, enemies=quadrant.commanders, rotationAngle=Commander.ROTATION_ANGLE)
        self.torpedoes.update()
        self.torpedoExplosions.update()
        self.torpedoFollowers.update()

        self._handleTorpedoHits(quadrant, enemies=quadrant.commanders)
        self._handleTorpedoMisses(quadrant, enemies=quadrant.commanders)
        self._handleMissRemoval(quadrant, cast(Misses, self._misses))

    def _getTorpedoToFire(self, enemy: Enemy, enterprise: Enterprise) -> BaseEnemyTorpedo:
        """
        Must be implemented by subclass to create correct type of torpedo

        Args:
            enemy:      The Klingon, Commander, or Super Commander that is firing
            enterprise: Where Captain Kirk is waiting

        Returns:  A torpedo of the correct kind
        """
        klingonPoint:    ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)
        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)

        speeds: TorpedoSpeeds = self._intelligence.getTorpedoSpeeds()

        commanderTorpedo: CommanderTorpedo = CommanderTorpedo(speed=speeds.commander)

        commanderTorpedo.center_x = klingonPoint.x
        commanderTorpedo.center_y = klingonPoint.y
        commanderTorpedo.inMotion = True
        commanderTorpedo.destinationPoint  = enterprisePoint
        commanderTorpedo.firedFromPosition = enemy.gameCoordinates
        commanderTorpedo.firedBy   = enemy.id
        commanderTorpedo.followers = self.torpedoFollowers

        return commanderTorpedo

    def _getTorpedoExplosion(self) -> BaseTorpedoExplosion:
        """
        Must be implemented by subclass to create correct type of torpedo explosion

        Returns: An explosion of the correct type

        """
        return CommanderTorpedoExplosion(textureList=self._explosionTextures)

    def _getTorpedoMiss(self) -> BaseMiss:
        """
        Implement empty base class method

        Returns:  An appropriate 'miss' sprite
        """
        return CommanderTorpedoMiss(placedTime=self._gameEngine.gameClock)

    def _playCannotFireSound(self):
        """
        We must implement this
        """
        self._soundCommanderCannotFire.play(self._gameSettings.soundVolume.value)

    def _playTorpedoFiredSound(self):
        """
        We must implement this
        """
        self._soundCommanderTorpedo.play(self._gameSettings.soundVolume.value)

    def _playTorpedoExplodedSound(self):
        """
        We must implement this
        """
        pass

    def _loadSounds(self):

        self._soundCommanderTorpedo    = BaseMediator.loadSound(bareFileName='CommanderTorpedo.wav')
        self._soundCommanderCannotFire = BaseMediator.loadSound(bareFileName='CommanderCannotFire.wav')

    def _loadTorpedoExplosionTextures(self) -> TextureList:

        nColumns:  int = 5
        tileCount: int = 23
        spriteWidth:  int = 64
        spriteHeight: int = 64
        bareFileName: str = f'CommanderTorpedoExplosionSpriteSheet.png'
        fqFileName:   str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

        textureList: TextureList = cast(TextureList, load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount))

        return textureList
