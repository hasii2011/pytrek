
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sprite
from arcade import SpriteList
from arcade import check_for_collision_with_list

from arcade import load_spritesheet

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType

from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.PhotonTorpedoExplosion import PhotonTorpedoExplosion
from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.PhotonTorpedo import PhotonTorpedo
from pytrek.gui.gamepieces.PhotonTorpedoMiss import PhotonTorpedoMiss

from pytrek.mediators.base.BaseMediator import LineOfSightResponse
from pytrek.mediators.base.MissesMediator import MissesMediator
from pytrek.mediators.base.MissesMediator import Misses
from pytrek.mediators.base.MissesMediator import Torpedoes

from pytrek.LocateResources import LocateResources

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.model.Quadrant import Quadrant

from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds


class EnterpriseTorpedoMediator(MissesMediator):

    def __init__(self):

        self.logger:        Logger       = getLogger(__name__)
        self._soundMachine: SoundMachine = SoundMachine()
        super().__init__()

        self._torpedoes:  SpriteList = SpriteList()
        self._misses:     SpriteList = SpriteList()
        self._explosions: SpriteList = SpriteList()

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
            self._soundMachine.playSound(SoundType.UnableToComply)
            self._messageConsole.displayMessage("You are out of photon torpedoes!!")
            return  # Take a shortcut out of here

        self._messageConsole.displayMessage("Firing Torpedoes!!")

        enterprise:  Enterprise = quadrant.enterprise

        enemies: Enemies = Enemies([])
        enemies.extend(quadrant.klingons)
        enemies.extend(quadrant.commanders)
        enemies.extend(quadrant.superCommanders)

        numberOfEnemies: int = len(enemies)
        if numberOfEnemies == 0:
            self._messageConsole.displayMessage("Don't waste torpedoes.  Nothing to fire at")
            self._soundMachine.playSound(SoundType.Inaccurate)
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
                        self._soundMachine.playSound(SoundType.PhotonTorpedoMisfire)
                    else:
                        self._fireTorpedo(enterprise=enterprise, enemy=enemy)
                        self._soundMachine.playSound(SoundType.PhotonTorpedoFired)
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
                    killerTorpedo: PhotonTorpedo = cast(PhotonTorpedo, sprite)
                    self.logger.info(f'{killerTorpedo.id} hit')

                    self.__doExplosion(killerTorpedo)

                    killerTorpedo.remove_from_sprite_lists()

                    self.__damageOrKillEnemy(enterprise, enemy)

        quadrant.removeDeadEnemies()

    def _handleTorpedoMisses(self, quadrant: Quadrant):

        torpedoDuds: List[BaseEnemyTorpedo] = self._findTorpedoMisses(cast(Torpedoes, self._torpedoes))

        for baseTorpedo in torpedoDuds:
            torpedoDud: PhotonTorpedo = cast(PhotonTorpedo, baseTorpedo)
            self._messageConsole.displayMessage(f'{torpedoDud.id} missed {torpedoDud.firedAt} !!!!')

            miss: PhotonTorpedoMiss = PhotonTorpedoMiss(placedTime=self._gameEngine.gameClock)
            self._placeMiss(quadrant=quadrant, torpedoDud=torpedoDud, miss=miss)
            self._soundMachine.playSound(SoundType.PhotonTorpedoMisfire)
            self._misses.append(miss)

            torpedoDud.remove_from_sprite_lists()

    def _pointAtEnemy(self, enemy: Enemy, enterprise: Enterprise):

        self._pointAtTarget(shooter=enterprise, target=enemy)
        self._messageConsole.displayMessage(f'Enterprise firing on course {enterprise.angle:.2f}')

    def _fireTorpedo(self, enterprise: Enterprise, enemy: Enemy):

        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        klingonPoint:    ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)

        speeds: TorpedoSpeeds      = self._intelligence.getTorpedoSpeeds(playerType=self._gameState.playerType)
        torpedo: PhotonTorpedo = PhotonTorpedo(speed=speeds.enterprise)

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
        bareFileName: str = f'PhotonTorpedoExplosionSpriteSheet.png'
        fqFileName:   str = LocateResources.getImagePath(bareFileName=bareFileName)

        explosions: TextureList = cast(TextureList, load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount))

        return explosions

    def _doWeHaveLineOfSight(self, quadrant: Quadrant, startingPoint: ArcadePoint, endPoint: ArcadePoint) -> LineOfSightResponse:
        """
        Check to see if a planet or a StarBase prevents
        the Enterprise from shooting at the enemy

        Args:
            startingPoint:

        Returns:  `True` if no obstructions, else `False`
        """
        obstacles: SpriteList = SpriteList()
        if quadrant.hasPlanet is True:
            obstacles.append(quadrant.planet)
        if quadrant.hasStarBase is True:
            obstacles.append(quadrant.starBase)

        results: LineOfSightResponse = self._hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.info(f'{results=}')
        return results

    def __doExplosion(self, killerTorpedo: PhotonTorpedo):

        explosion: PhotonTorpedoExplosion = PhotonTorpedoExplosion(textureList=self._torpedoExplosionTextures)
        explosion.center_x = killerTorpedo.center_x
        explosion.center_y = killerTorpedo.center_y

        self._explosions.append(explosion)

        self._soundMachine.playSound(SoundType.PhotonTorpedoExploded)

    def __damageOrKillEnemy(self, enterprise: Enterprise, enemy: Enemy):

        kHit: float = self._gameEngine.computeHitValueOnKlingon(enterprisePosition=enterprise.gameCoordinates,
                                                                klingonPosition=enemy.gameCoordinates,
                                                                klingonPower=enemy.power)
        enemy.power -= kHit
        self._messageConsole.displayMessage(f'{enemy.id} took hit: {kHit:.2f}  remaining: {enemy.power:.2f}')
        if enemy.power <= 0:
            self._messageConsole.displayMessage(f'{enemy.id} destroyed')
            enemy.power = 0
            enemy.remove_from_sprite_lists()

            self._decrementAppropriateEnemyCount(enemy)

    def _decrementAppropriateEnemyCount(self, enemy):
        from pytrek.gui.gamepieces.klingon.Klingon import Klingon
        from pytrek.gui.gamepieces.commander.Commander import Commander
        from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander

        if isinstance(enemy, Klingon) is True:
            self._gameState.remainingKlingons -= 1
        elif isinstance(enemy, Commander) is True:
            self._gameState.remainingCommanders -= 1
        elif isinstance(enemy, SuperCommander) is True:
            self._gameState.remainingSuperCommanders -= 1
        else:
            assert False, f'Unknown enemy type: {enemy.id}'
