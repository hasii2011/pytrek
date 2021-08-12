
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import Sprite
from arcade import SpriteList
from arcade import check_for_collision_with_list

from arcade import load_spritesheet

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.EnterpriseTorpedoExplosion import EnterpriseTorpedoExplosion
from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.EnterpriseTorpedo import EnterpriseTorpedo
from pytrek.gui.gamepieces.EnterpriseTorpedoMiss import EnterpriseTorpedoMiss
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList

from pytrek.mediators.base.BaseMediator import BaseMediator
from pytrek.mediators.base.BaseMediator import LineOfSightResponse
from pytrek.mediators.base.BaseMediator import Misses
from pytrek.mediators.base.BaseMediator import Torpedoes

from pytrek.LocateResources import LocateResources

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.model.Quadrant import Quadrant

from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds


class EnterpriseTorpedoMediator(BaseMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)
        super().__init__()

        self._torpedoes:  SpriteList = SpriteList()
        self._misses:     SpriteList = SpriteList()
        self._explosions: SpriteList = SpriteList()

        self._photonTorpedoFired:  Sound = cast(Sound, None)
        self._explosionSound:      Sound = cast(Sound, None)
        self._noKlingonsSound:     Sound = cast(Sound, None)
        self._torpedoMisfire:      Sound = cast(Sound, None)
        self._torpedoMiss:         Sound = cast(Sound, None)
        self._soundUnableToComply: Sound = cast(Sound, None)

        self._loadSounds()

        self._torpedoExplosionTextures: TextureList = self._loadPhotonTorpedoExplosions()

    @property
    def torpedoExplosionTextures(self) -> TextureList:
        return self._torpedoExplosionTextures

    # noinspection PyUnusedLocal
    def draw(self, quadrant: Quadrant):
        self._torpedoes.draw()
        self._explosions.draw()
        self._misses.draw()

    def update(self, quadrant: Quadrant):
        self._torpedoes.update()
        self._explosions.update()
        self._handleTorpedoHits(quadrant=quadrant)
        self._handleTorpedoMisses(quadrant=quadrant)
        self._handleMissRemoval(quadrant, cast(Misses, self._misses))

    def fireEnterpriseTorpedoesAtKlingons(self, quadrant: Quadrant):

        if self._gameState.torpedoCount <= 0:
            self._soundUnableToComply.play(volume=self._gameSettings.soundVolume.value)
            self._messageConsole.displayMessage("You are out of photon torpedoes!!")
            return  # Take a short cut out of here

        self._messageConsole.displayMessage("Firing Torpedoes!!")

        soundVolume: float      = self._gameSettings.soundVolume.value
        enterprise:  Enterprise = quadrant.enterprise

        enemies: Enemies = Enemies([])
        enemies.extend(quadrant.klingons)
        enemies.extend(quadrant.commanders)
        enemies.extend(quadrant.superCommanders)

        numberOfEnemies: int = len(enemies)
        if numberOfEnemies == 0:
            self._messageConsole.displayMessage("Don't waste torpedoes.  Nothing to fire at")
            self._noKlingonsSound.play(volume=soundVolume)
        else:
            startingPoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
            #
            #  Only fire as many torpedoes as we have available
            #  TODO:  Fire only 'N' torpedoes at randomly selected enemies
            #
            for enemy in enemies:
                endPoint: ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)

                clearLineOfSight: LineOfSightResponse = self._doWeHaveLineOfSight(quadrant, startingPoint, endPoint)
                if clearLineOfSight.answer is True:
                    self._pointAtEnemy(enterprise=enterprise, enemy=enemy)
                    if self._intelligence.rand() <= self._gameSettings.photonTorpedoMisfireRate:
                        self._messageConsole.displayMessage(f'Torpedo pointed at {enemy} misfired')
                        self._torpedoMisfire.play(volume=soundVolume)
                    else:
                        self._fireTorpedo(enterprise=enterprise, enemy=enemy)
                        self._photonTorpedoFired.play(volume=soundVolume)
                        self._gameState.torpedoCount -= 1
                else:
                    msg: str = (
                        f'Cannot fire at {enemy.id} '
                        f'because a {clearLineOfSight.obstacle.id} is in the way'
                    )
                    self._messageConsole.displayMessage(message=msg)
                    self.logger.info(msg)
            enterprise.angle = 0

    def _handleTorpedoHits(self, quadrant: Quadrant):

        enemies: Enemies = Enemies([])

        enemies.extend(quadrant.klingons)
        enemies.extend(quadrant.commanders)
        enemies.extend(quadrant.superCommanders)

        enterprise: Enterprise = quadrant.enterprise
        for badGuy in enemies:
            enemy: Enemy = cast(Enemy, badGuy)
            if enemy.power > 0:
                expendedTorpedoes: List[Sprite] = check_for_collision_with_list(sprite=enemy, sprite_list=self._torpedoes)

                for sprite in expendedTorpedoes:
                    killerTorpedo: EnterpriseTorpedo = cast(EnterpriseTorpedo, sprite)
                    self.logger.info(f'{killerTorpedo.id} hit')

                    self.__doExplosion(killerTorpedo)

                    killerTorpedo.remove_from_sprite_lists()

                    self.__damageOrKillEnemy(enterprise, enemy)

        quadrant.removeDeadEnemies()

    def _handleTorpedoMisses(self, quadrant: Quadrant):

        torpedoDuds: List[BaseEnemyTorpedo] = self._findTorpedoMisses(cast(Torpedoes, self._torpedoes))

        for baseTorpedo in torpedoDuds:
            torpedoDud: EnterpriseTorpedo = cast(EnterpriseTorpedo, baseTorpedo)
            self._messageConsole.displayMessage(f'{torpedoDud.id} missed {torpedoDud.firedAt} !!!!')

            miss: EnterpriseTorpedoMiss = EnterpriseTorpedoMiss(placedTime=self._gameEngine.gameClock)
            self._placeMiss(quadrant=quadrant, torpedoDud=torpedoDud, miss=miss)
            self._torpedoMiss.play(self._gameSettings.soundVolume.value)
            self._misses.append(miss)

            torpedoDud.remove_from_sprite_lists()

    def _loadSounds(self):

        self._photonTorpedoFired  = self._loadSound(bareFileName='photonTorpedo.wav')
        self._explosionSound      = self._loadSound(bareFileName='SmallExplosion.wav')
        self._noKlingonsSound     = self._loadSound(bareFileName='inaccurateError.wav')
        self._torpedoMisfire      = self._loadSound(bareFileName='PhotonTorpedoMisfire.wav')
        self._torpedoMiss         = self._loadSound(bareFileName='PhotonTorpedoMiss.wav')
        self._soundUnableToComply = self._loadSound(bareFileName='unableToComply.wav')

    def _pointAtEnemy(self, enemy: Enemy, enterprise: Enterprise):

        self._pointAtTarget(shooter=enterprise, target=enemy)
        self._messageConsole.displayMessage(f'Enterprise firing on course {enterprise.angle:.2f}')

    def _fireTorpedo(self, enterprise: Enterprise, enemy: Enemy):

        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        klingonPoint:    ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)

        speeds: TorpedoSpeeds      = self._intelligence.getTorpedoSpeeds()
        torpedo: EnterpriseTorpedo = EnterpriseTorpedo(speed=speeds.enterprise)

        torpedo.center_x = enterprisePoint.x
        torpedo.center_y = enterprisePoint.y
        torpedo.inMotion = True
        torpedo.firedAt  = enemy.id
        torpedo.destinationPoint = klingonPoint

        self._torpedoes.append(torpedo)
        self._messageConsole.displayMessage(f'Enterprise fire from: {enterprise.gameCoordinates} at Klingon {enemy.id}')

    def _loadPhotonTorpedoExplosions(self) -> TextureList:
        """
        Cache the torpedo explosion textures

        Returns:  The texture list
        """
        nColumns:  int = 8
        tileCount: int = 21
        spriteWidth:  int = 128
        spriteHeight: int = 128
        bareFileName: str = f'EnterpriseTorpedoExplosionSheet.png'
        fqFileName:   str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

        explosions: TextureList = cast(TextureList, load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount))

        return explosions

    def _doWeHaveLineOfSight(self, quadrant: Quadrant, startingPoint: ArcadePoint, endPoint: ArcadePoint) -> LineOfSightResponse:
        """
        Check to see if planets or StarBases prevent
        the Enterprise from shooting at the enemy

        Args:
            startingPoint:

        Returns:  `True` if no obstructions, else `False`
        """
        obstacles: SpriteList = SpriteList()
        if quadrant.hasPlanet is True:
            obstacles.append(quadrant.planet)

        results: LineOfSightResponse = self._hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.info(f'{results=}')
        return results

    def __doExplosion(self, killerTorpedo: EnterpriseTorpedo):

        explosion: EnterpriseTorpedoExplosion = EnterpriseTorpedoExplosion(textureList=self._torpedoExplosionTextures)
        explosion.center_x = killerTorpedo.center_x
        explosion.center_y = killerTorpedo.center_y

        self._explosions.append(explosion)

        self._explosionSound.play(self._gameSettings.soundVolume.value)

    def __damageOrKillEnemy(self, enterprise: Enterprise, enemy: Enemy):

        kHit: float = self._computer.computeHitValueOnKlingon(enterprisePosition=enterprise.gameCoordinates,
                                                              klingonPosition=enemy.gameCoordinates,
                                                              klingonPower=enemy.power)
        enemy.power -= kHit
        self._messageConsole.displayMessage(f'{enemy.id} took hit: {kHit:.2f}  remaining: {enemy.power:.2f}')
        if enemy.power <= 0:
            self._messageConsole.displayMessage(f'{enemy.id} destroyed')
            enemy.remove_from_sprite_lists()
            enemy.power = 0
