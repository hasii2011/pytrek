
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import Sprite
from arcade import SpriteList
from arcade import Texture
from arcade import check_for_collision_with_list

from arcade import load_spritesheet

from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.Explosion import Explosion
from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.gui.gamepieces.PhotonTorpedo import PhotonTorpedo
from pytrek.gui.gamepieces.PhotonTorpedoMiss import PhotonTorpedoMiss

from pytrek.mediators.BaseMediator import BaseMediator
from pytrek.mediators.BaseMediator import LineOfSightResponse
from pytrek.mediators.BaseMediator import Misses
from pytrek.mediators.BaseMediator import Torpedoes

from pytrek.model.Quadrant import Quadrant


class PhotonTorpedoMediator(BaseMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)
        super().__init__()

        self._torpedoes:  SpriteList = SpriteList()
        self._misses:     SpriteList = SpriteList()
        self._explosions: SpriteList = SpriteList()

        self._loadSounds()

        self._torpedoTextures: List[Texture] = self._loadPhotonTorpedoExplosions()

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

        self._messageConsole.displayMessage("Firing Torpedoes!!")

        soundVolume: float      = self._gameSettings.soundVolume.value

        enterprise: Enterprise = quadrant.enterprise
        # klingons:   Klingons   = quadrant.klingons

        enemies: Enemies = Enemies([])
        # noinspection PyTypeChecker
        enemies = enemies + quadrant.klingons + quadrant.commanders

        if len(enemies) == 0:
            self._messageConsole.displayMessage("Don't waste torpedoes.  Nothing to fire at")
            self._noKlingonsSound.play(volume=soundVolume)
        else:
            startingPoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
            for enemy in enemies:
                endPoint: ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)

                clearLineOfSight: LineOfSightResponse = self._doWeHaveLineOfSight(quadrant, startingPoint, endPoint)
                if clearLineOfSight.answer is True:
                    enemy: Klingon = cast(Klingon, enemy)
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

        # klingons:   Klingons  = quadrant.klingons
        enemies: Enemies = Enemies([])

        enemies.extend(quadrant.klingons)
        enemies.extend(quadrant.commanders)

        enterprise: Enterprise = quadrant.enterprise
        for enemy in enemies:
            enemy: Enemy = cast(Enemy, enemy)
            if enemy.power > 0:
                expendedTorpedoes: List[Sprite] = check_for_collision_with_list(sprite=enemy, sprite_list=self._torpedoes)

                for killerTorpedo in expendedTorpedoes:
                    killerTorpedo: PhotonTorpedo = cast(PhotonTorpedo, killerTorpedo)
                    self.logger.info(f'{killerTorpedo.id} hit')

                    self.__doExplosion(killerTorpedo)

                    killerTorpedo.remove_from_sprite_lists()

                    self.__damageOrKillEnemy(enterprise, enemy)

        quadrant.removeDeadEnemies()

    def _handleTorpedoMisses(self, quadrant: Quadrant):

        torpedoDuds: List[PhotonTorpedo] = self._findTorpedoMisses(cast(Torpedoes, self._torpedoes))

        for torpedoDud in torpedoDuds:

            self._messageConsole.displayMessage(f'{torpedoDud.id} missed {torpedoDud.firedAt} !!!!')

            miss: PhotonTorpedoMiss = PhotonTorpedoMiss(placedTime=self._gameEngine.gameClock)
            self._placeMiss(quadrant=quadrant, torpedoDud=torpedoDud, miss=miss)
            self._misses.append(miss)

            torpedoDud.remove_from_sprite_lists()

    def _loadSounds(self):

        self._photonTorpedoFired: Sound = self.__loadSound('photonTorpedo.wav')
        self._explosionSound:     Sound = self.__loadSound('SmallExplosion.wav')
        self._noKlingonsSound:    Sound = self.__loadSound('inaccurateError.wav')
        self._torpedoMisfire:     Sound = self.__loadSound('PhotonTorpedoMisfire.wav')

    def _pointAtEnemy(self, enemy: Enemy, enterprise: Enterprise):

        currentPoint:     ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        destinationPoint: ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)

        normalAngle: float = self._computer.computeAngleToTarget(shooter=currentPoint, deadMeat=destinationPoint)
        enterprise.angle = normalAngle + 125

        self._messageConsole.displayMessage(f'Enterprise firing on course {enterprise.angle:.2f}')

    def _fireTorpedo(self, enterprise: Enterprise, enemy: Enemy):

        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        klingonPoint:    ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)

        torpedo: PhotonTorpedo = PhotonTorpedo()

        torpedo.center_x = enterprisePoint.x
        torpedo.center_y = enterprisePoint.y
        torpedo.inMotion = True
        torpedo.firedAt  = enemy.id
        torpedo.destinationPoint = klingonPoint

        self._torpedoes.append(torpedo)
        self._messageConsole.displayMessage(f'Enterprise fire from: {enterprise.gameCoordinates} at Klingon {enemy.id}')

    def _loadPhotonTorpedoExplosions(self) -> List[Texture]:
        """
        Cache the torpedo explosion textures

        Returns:  The texture list
        """
        nColumns:  int = 8
        tileCount: int = 21
        spriteWidth:  int = 128
        spriteHeight: int = 128
        bareFileName: str = f'PhotonTorpedoExplosionSprites.png'
        fqFileName:   str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

        explosions: List[Texture] = load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount)

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
            obstacles.append(quadrant._planet)

        results: LineOfSightResponse = self._hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.info(f'{results=}')
        return results

    def __doExplosion(self, killerTorpedo: PhotonTorpedo):

        explosion: Explosion = Explosion(textureList=self._torpedoTextures, sound=self._explosionSound)
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

    def __loadSound(self, bareFileName: str) -> Sound:

        fqFileName: str   = LocateResources.getResourcesPath(LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName)
        sound:      Sound = Sound(fqFileName)

        return sound
