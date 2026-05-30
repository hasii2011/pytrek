
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import SpriteSheet

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemy

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss
from pytrek.gui.gamepieces.base.BaseAnimator import TextureList
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import BaseTorpedoExplosion

from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander
from pytrek.gui.gamepieces.supercommander.SuperCommanderTorpedo import SuperCommanderTorpedo
from pytrek.gui.gamepieces.supercommander.SuperCommanderTorpedoExplosion import SuperCommanderTorpedoExplosion
from pytrek.gui.gamepieces.supercommander.SuperCommanderTorpedoMiss import SuperCommanderTorpedoMiss

from pytrek.mediators.base.MissesMediator import Misses
from pytrek.mediators.base.BaseTorpedoMediator import BaseTorpedoMediator

from pytrek.model.Quadrant import Quadrant

from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.LocateResources import LocateResources


class SuperCommanderTorpedoMediator(BaseTorpedoMediator):
    """
    Handles photon torpedo combat operations initiated by Klingon Super Commander
    ships targeting the USS Enterprise.

    This mediator:
    - Preloads and grid-aligns Super Commander torpedo explosions
    - Determines if Super Commanders in the current quadrant need to fire torpedoes.
    - Manages the drawing, updating, and lifecycle of active Super Commander torpedoes,
      torpedo follower trails, explosions, and miss indicators.
    - Instantiates specific Super Commander torpedo, explosion, and miss game piece sprites.
    - Plays audio cues for Super Commander torpedo firing attempts and execution.
    """

    def __init__(self):

        self.logger:        Logger       = getLogger(__name__)
        self._soundMachine: SoundMachine = SoundMachine()
        super().__init__()

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
        self._fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant, enemies=quadrant.superCommanders, rotationAngle=SuperCommander.ROTATION_ANGLE)
        self.torpedoes.update()
        self.torpedoFollowers.update()
        self.torpedoExplosions.update()

        self._handleTorpedoHits(quadrant, enemies=quadrant.superCommanders)
        self._handleTorpedoMisses(quadrant, enemies=quadrant.superCommanders)
        self._handleMissRemoval(quadrant, cast(Misses, self._misses))       # noqa

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

        speeds: TorpedoSpeeds = self._intelligence.getTorpedoSpeeds(playerType=self._gameState.playerType)

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
        return SuperCommanderTorpedoMiss(placedTime=self._gameEngine.gameClock)

    def _playCannotFireSound(self):
        """
        We must implement this
        """
        self._soundMachine.playSound(SoundType.SuperCommanderCannotFire)

    def _playTorpedoFiredSound(self):
        """
        We must implement this
        """
        self._soundMachine.playSound(SoundType.SuperCommanderTorpedo)

    def _playTorpedoExplodedSound(self):
        """
        We must implement this
        """
        pass

    def _getTorpedoExplosion(self) -> BaseTorpedoExplosion:
        """
        We must implement this

        Returns: An explosion of the correct type

        """
        return SuperCommanderTorpedoExplosion(textureList=self._explosionTextures)

    def _loadTorpedoExplosionTextures(self) -> TextureList:

        nColumns:  int = 3
        tileCount: int = 9
        spriteWidth:  int = 32
        spriteHeight: int = 32
        bareFileName: str = f'SuperCommanderTorpedoExplosionSpriteSheet.png'
        fqFileName:   str = LocateResources.getImagePath(bareFileName=bareFileName)

        # textureList: TextureList = cast(TextureList, load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount))

        sheet: SpriteSheet = SpriteSheet(fqFileName)

        textureList: TextureList = cast(TextureList,
                                        sheet.get_texture_grid(
                                            size=(spriteWidth, spriteHeight),
                                            columns=nColumns,
                                            count=tileCount
                                        )
                                        )

        return textureList
