
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import Sprite
from arcade import SpriteList
from arcade import check_for_collision_with_list

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.ShieldHitData import ShieldHitData
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices

from pytrek.gui.gamepieces.base.BaseEnemy import BaseEnemy
from pytrek.gui.gamepieces.base.BaseEnemy import EnemyId
from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import BaseTorpedoExplosion
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList
from pytrek.gui.gamepieces.base.BaseTorpedoFollower import BaseTorpedoFollower
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.gui.gamepieces.GamePieceTypes import Enemy

from pytrek.mediators.base.MissesMediator import MissesMediator
from pytrek.mediators.base.MissesMediator import LineOfSightResponse
from pytrek.mediators.base.MissesMediator import Torpedoes

from pytrek.model.Quadrant import Quadrant

from pytrek.Constants import DEFAULT_FULL_SHIELDS


class BaseTorpedoMediator(MissesMediator):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):

        super().__init__()

        self.logger: Logger = BaseTorpedoMediator.clsLogger

        self._devices: Devices = Devices()

        self._torpedoes:        SpriteList = SpriteList()
        self._explosions:       SpriteList = SpriteList()
        self._torpedoFollowers: SpriteList = SpriteList(is_static=True)
        self._misses:           SpriteList = SpriteList()

        self._lastTimeCheck:  float = self._gameEngine.gameClock / 1000
        self._soundShieldHit: Sound = self._loadSound(bareFileName='ShieldHit.wav')

        self.logger.info(f'{self._lastTimeCheck=}')

    @property
    def torpedoes(self) -> SpriteList:
        return self._torpedoes

    @torpedoes.setter
    def torpedoes(self, newList: SpriteList):
        """
        Args:
            newList:
        """
        self._torpedoes = newList

    @property
    def torpedoFollowers(self) -> SpriteList:
        return self._torpedoFollowers

    @torpedoFollowers.setter
    def torpedoFollowers(self, newValues: SpriteList):
        self._torpedoFollowers = newValues

    @property
    def torpedoDuds(self) -> SpriteList:
        return self._misses

    @torpedoDuds.setter
    def torpedoDuds(self, newValues: SpriteList):
        self._misses = newValues

    @property
    def torpedoExplosions(self) -> SpriteList:
        return self._explosions

    def draw(self):
        """
        Implemented by subclass
        """
        pass

    def update(self, quadrant: Quadrant):
        """
        Implemented by subclass
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

    def _loadTorpedoExplosionTextures(self) -> TextureList:
        """
        Subclasses must implement this method

        Returns:  The textures (images) that display an explosion
        """
        pass

    def _getTorpedoExplosion(self) -> BaseTorpedoExplosion:
        """
        Must be implemented by subclass to create correct type of torpedo explosion

        Returns: An explosion of the correct type

        """
        pass

    def _getTorpedoMiss(self) -> BaseMiss:
        """
        Implemented by subclass

        Returns:  An appropriate 'miss' sprite
        """
        pass

    def _playCannotFireSound(self):
        """
        Implemented by subclass
        """
        pass

    def _playTorpedoFiredSound(self):
        """
        Implemented by subclass
        """
        pass

    def _playTorpedoExplodedSound(self):
        """
        Implemented by subclass
        """
        pass

    def _fireTorpedoesAtEnterpriseIfNecessary(self, quadrant: Quadrant, enemies: Enemies, rotationAngle: int = 125):
        """

        Args:
            quadrant:   Quadrant we are in
            enemies:    The enemies to fire from
            rotationAngle: The offset to add to the image when pointing at enterprise

        Returns:

        """

        currentTime: float = self._gameEngine.gameClock

        for enemy in enemies:
            deltaClockTime: float = currentTime - enemy.lastTimeCheck
            if deltaClockTime > enemy.firingInterval:
                self.logger.debug(f'Time for {enemy} to fire torpedoes')

                endPoint:            ArcadePoint = ArcadePoint(x=quadrant.enterprise.center_x, y=quadrant.enterprise.center_y)
                lineOfSightResponse: LineOfSightResponse = self._doWeHaveLineOfSight(quadrant, shooter=enemy, endPoint=endPoint)
                if lineOfSightResponse.answer is True:
                    self._pointAtEnterprise(enemy=enemy, enterprise=quadrant.enterprise, rotationAngle=rotationAngle)
                    self._fireTorpedo(enemy=enemy, enterprise=quadrant.enterprise)
                else:
                    self._playCannotFireSound()
                    self._messageConsole.displayMessage(f'{enemy.id} cannot shoot, blocked by {lineOfSightResponse.obstacle.id}')

                enemy.lastTimeCheck = round(currentTime)

    def _fireTorpedo(self, enemy: Enemy, enterprise: Enterprise):
        """
        Args:
            enemy:      Who is firing it
            enterprise: The poor lowly enterprise is the target
        """

        self.logger.info(f'{enemy.id} @ {enemy.gameCoordinates} firing; Enterprise @ {enterprise.gameCoordinates}')
        self._messageConsole.displayMessage(f'{enemy.id} @ {enemy.gameCoordinates} firing; Enterprise @ {enterprise.gameCoordinates}')

        enemyTorpedo: BaseEnemyTorpedo = self._getTorpedoToFire(enemy, enterprise)

        self.torpedoes.append(enemyTorpedo)
        self._playTorpedoFiredSound()

        self.logger.info(f'{enemyTorpedo.firedFromPosition=}')

    def _handleTorpedoMisses(self, quadrant: Quadrant, enemies: Enemies):

        torpedoDuds: List[BaseEnemyTorpedo] = self._findTorpedoMisses(cast(Torpedoes, self.torpedoes))

        for torpedoDud in torpedoDuds:
            self._removeTorpedoFollowers(enemyTorpedo=torpedoDud)

            firedBy: EnemyId = torpedoDud.firedBy

            shootingKlingon: BaseEnemy = self._findFiringEnemy(enemyId=firedBy, enemies=enemies)
            if shootingKlingon is not None:
                self._messageConsole.displayMessage(f'{shootingKlingon.id} missed !!!!')
                self._placeTorpedoMiss(quadrant=quadrant, torpedoDud=torpedoDud)
                shootingKlingon.angle = 0
            torpedoDud.remove_from_sprite_lists()

    def _removeTorpedoFollowers(self, enemyTorpedo: BaseEnemyTorpedo):

        followersToRemove: List[BaseTorpedoFollower] = []
        for sprite in self.torpedoFollowers:
            follower: BaseTorpedoFollower = cast(BaseTorpedoFollower, sprite)
            if follower.following == enemyTorpedo.id:
                self.logger.debug(f'Removing follower: {follower.id}')
                followersToRemove.append(follower)

        for followerToRemove in followersToRemove:
            followerToRemove.remove_from_sprite_lists()

    def _placeTorpedoMiss(self, quadrant: Quadrant, torpedoDud: BaseEnemyTorpedo):

        miss: BaseMiss = self._getTorpedoMiss()

        self._placeMiss(quadrant=quadrant, torpedoDud=torpedoDud, miss=miss)
        self._misses.append(miss)

    def _doWeHaveLineOfSight(self, quadrant: Quadrant, shooter: Enemy, endPoint: ArcadePoint) -> LineOfSightResponse:

        startingPoint: ArcadePoint = ArcadePoint(x=shooter.center_x, y=shooter.center_y)
        obstacles:     SpriteList  = SpriteList()

        if quadrant.hasPlanet is True:
            obstacles.append(quadrant.planet)

        otherEnemies: Enemies = self.__buildEligibleEnemyObstacles(shooter=shooter, enemies=quadrant.klingons)

        obstacles.extend(otherEnemies)

        results: LineOfSightResponse = self._hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.debug(f'{results=}')
        return results

    def _findFiringEnemy(self, enemyId: EnemyId, enemies: Enemies) -> Enemy:
        """

        Args:
            enemyId:    The ID of the enemy that fired
            enemies:    The list we are searching

        Returns:  May return 'None' if the Enterprise killed him
        """

        fndEnemy: Enemy = cast(Enemy, None)
        for enemy in enemies:
            # enemy: Enemy = cast(Enemy, enemy)
            if enemy.id == enemyId:
                fndEnemy = enemy
                break

        return fndEnemy

    def _handleTorpedoHits(self, quadrant: Quadrant, enemies: Enemies):
        """
        For each torpedo use arcade to determine collision

         * Remove it's followers
         * Determine which Klingon fired it
         * Determine how severe of a hit it was
         * Adjust the Enterprise shield power value or the Enterprise power value itself
        Args:
            quadrant:  The current quadrant we are in
        """
        expendedTorpedoes: List[Sprite] = check_for_collision_with_list(sprite=quadrant.enterprise, sprite_list=self.torpedoes)
        for sprite in expendedTorpedoes:
            expendedTorpedo: BaseEnemyTorpedo = cast(BaseEnemyTorpedo, sprite)
            self.logger.info(f'{expendedTorpedo.id} arrived at destination')
            self._removeTorpedoFollowers(enemyTorpedo=expendedTorpedo)

            firedBy: EnemyId = expendedTorpedo.firedBy
            shootingEnemy: BaseEnemy = self._findFiringEnemy(enemyId=firedBy, enemies=enemies)

            if shootingEnemy is not None:
                shootingEnemy.angle = 0
                self._computeDamage(quadrant, shootingEnemy)

            self.__doExplosion(expendedTorpedo=expendedTorpedo)

            expendedTorpedo.remove_from_sprite_lists()

            if self._gameState.energy <= 0:
                # alert(theMessage='Game Over!  The Enterprise is out of energy')
                # sys.exit()
                pass

        # damagedDeviceType: DeviceType = self._intelligence.fryDevice(shieldHitData.degradedTorpedoHitValue)
        # if damagedDeviceType is not None:
        #     self.messageConsole.addText(f"Device: {damagedDeviceType} damaged")
        #
        # if damagedDeviceType == DeviceType.Shields:
        #     self.messageConsole.addText("Shield energy transferred to Enterprise")
        #     self.statistics.energy += self.statistics.shieldEnergy
        #     self.statistics.shieldEnergy = 0

    def _computeDamage(self, quadrant: Quadrant, shooter: BaseEnemy):

        hitValue: float = self._computer.computeHitValueOnEnterprise(enemyPosition=shooter.gameCoordinates,
                                                                     enterprisePosition=quadrant.enterpriseCoordinates,
                                                                     enemyPower=shooter.power)
        self.logger.debug(f"Original Hit Value: {hitValue:.4f} {shooter=}")
        if self._devices.getDeviceStatus(DeviceType.Shields) == DeviceStatus.Up:
            shieldHitData: ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=hitValue)
        else:
            shieldHitData = ShieldHitData(degradedTorpedoHitValue=hitValue, shieldAbsorptionValue=0.0)

        shieldAbsorptionValue   = shieldHitData.shieldAbsorptionValue
        degradedTorpedoHitValue = shieldHitData.degradedTorpedoHitValue

        self._soundShieldHit.play()
        self._gameEngine.degradeShields(shieldAbsorptionValue)

        shieldPercentage: int = round((self._gameState.shieldEnergy / DEFAULT_FULL_SHIELDS) * 100)
        shieldMsg:        str = f"Shields at {shieldPercentage} percent.  Enterprise energy degraded by: {degradedTorpedoHitValue:.2f}"

        self._messageConsole.displayMessage(shieldMsg)
        self._gameEngine.degradeEnergyLevel(shieldHitData.degradedTorpedoHitValue)

    def _pointAtEnterprise(self, enemy: Enemy, enterprise: Enterprise, rotationAngle: int = 125):

        self._pointAtTarget(shooter=enemy, target=enterprise, rotationAngle=rotationAngle)

    def __buildEligibleEnemyObstacles(self, shooter: Enemy, enemies: Enemies) -> Enemies:
        """

        Returns:  A list of enemies excluding the shooter
        """
        obstacles: Enemies = Enemies([])
        for enemy in enemies:
            if enemy.id != shooter.id:
                obstacles.append(enemy)
        return obstacles

    def __doExplosion(self, expendedTorpedo: BaseEnemyTorpedo):

        self._playTorpedoExplodedSound()

        # TODO Super Commander not yet implemented
        explosion: BaseTorpedoExplosion = self._getTorpedoExplosion()
        if explosion is not None:
            explosion.center_x = expendedTorpedo.center_x
            explosion.center_y = expendedTorpedo.center_y

            self._explosions.append(explosion)
