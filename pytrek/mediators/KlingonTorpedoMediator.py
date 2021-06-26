
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import Sprite
from arcade import SpriteList
from arcade import check_for_collision_with_list

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.ShieldHitData import ShieldHitData

from pytrek.gui.gamepieces.BaseEnemy import EnemyId
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.gui.gamepieces.KlingonTorpedo import KlingonTorpedo
from pytrek.gui.gamepieces.KlingonTorpedoFollower import KlingonTorpedoFollower
from pytrek.gui.gamepieces.KlingonTorpedoMiss import KlingonTorpedoMiss

from pytrek.mediators.BaseMediator import LineOfSightResponse
from pytrek.mediators.BaseMediator import Misses
from pytrek.mediators.BaseMediator import Torpedoes
from pytrek.mediators.BaseTorpedoMediator import BaseTorpedoMediator

from pytrek.model.Quadrant import Quadrant

from pytrek.Constants import DEFAULT_FULL_SHIELDS


class KlingonTorpedoMediator(BaseTorpedoMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__()

        self._devices: Devices = Devices()

        self._soundKlingonTorpedo:    Sound = cast(Sound, None)
        self._soundShieldHit:         Sound = cast(Sound, None)
        self._soundKlingonCannotFire: Sound = cast(Sound, None)

        self._loadSounds()

    def draw(self):

        self.torpedoes.draw()
        self.torpedoFollowers.draw()
        self.torpedoDuds.draw()

    def update(self, quadrant: Quadrant):

        self._fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant)
        self.torpedoes.update()
        self.torpedoFollowers.update()

        self._handleKlingonTorpedoHits(quadrant)
        self._handleKlingonTorpedoMisses(quadrant)
        self._handleMissRemoval(quadrant, cast(Misses, self._misses))

    def _fireTorpedoesAtEnterpriseIfNecessary(self, quadrant: Quadrant):

        currentTime: float = self._gameEngine.gameClock

        klingons: List[Klingon] = quadrant.klingons
        for klingon in klingons:
            deltaClockTime: float = currentTime - klingon.lastTimeCheck
            if deltaClockTime > klingon.firingInterval:
                self.logger.debug(f'Time for {klingon} to fire torpedoes')

                endPoint:            ArcadePoint = ArcadePoint(x=quadrant.enterprise.center_x, y=quadrant.enterprise.center_y)
                lineOfSightResponse: LineOfSightResponse = self._doWeHaveLineOfSight(quadrant, shooter=klingon, endPoint=endPoint)
                if lineOfSightResponse.answer is True:
                    self.__pointAtEnterprise(klingon=klingon, enterprise=quadrant.enterprise)
                    self.__fireKlingonTorpedo(klingon=klingon, enterprise=quadrant.enterprise)
                else:
                    self._soundKlingonCannotFire.play(volume=self._gameSettings.soundVolume.value)
                    self._messageConsole.displayMessage(f'{klingon.id} cannot shoot, blocked by {lineOfSightResponse.obstacle.id}')

                klingon.lastTimeCheck = currentTime

    def _handleKlingonTorpedoHits(self, quadrant: Quadrant):
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
        for expendedTorpedo in expendedTorpedoes:

            expendedTorpedo: KlingonTorpedo = cast(KlingonTorpedo, expendedTorpedo)
            self.logger.info(f'{expendedTorpedo.id} arrived at destination')
            self._removeTorpedoFollowers(klingonTorpedo=expendedTorpedo)

            firedBy: EnemyId = expendedTorpedo.firedBy
            shootingKlingon: Klingon = self._findFiringKlingon(klingonId=firedBy)

            if shootingKlingon is not None:
                shootingKlingon.angle = 0
                hitValue: float = self._computer.computeHitValueOnEnterprise(klingonPosition=shootingKlingon.gameCoordinates,
                                                                             enterprisePosition=quadrant.enterpriseCoordinates,
                                                                             klingonPower=shootingKlingon.power)

                self.logger.debug(f"Original Hit Value: {hitValue:.4f} {shootingKlingon=}")

                if self._devices.getDeviceStatus(DeviceType.Shields) == DeviceStatus.Up:
                    shieldHitData: ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=hitValue)
                else:
                    shieldHitData: ShieldHitData = ShieldHitData(degradedTorpedoHitValue=hitValue, shieldAbsorptionValue=0.0)
                shieldAbsorptionValue   = shieldHitData.shieldAbsorptionValue
                degradedTorpedoHitValue = shieldHitData.degradedTorpedoHitValue

                self._soundShieldHit.play()
                self._gameEngine.degradeShields(shieldAbsorptionValue)
                shieldPercentage: int = round((self._gameState.shieldEnergy / DEFAULT_FULL_SHIELDS) * 100)

                shieldMsg: str = f"Shields at {shieldPercentage} percent.  Enterprise energy degraded by: {degradedTorpedoHitValue:.2f}"
                self._messageConsole.displayMessage(shieldMsg)

                self._gameEngine.degradeEnergyLevel(shieldHitData.degradedTorpedoHitValue)

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

    def _handleKlingonTorpedoMisses(self, quadrant: Quadrant):

        torpedoDuds: List[KlingonTorpedo] = self._findTorpedoMisses(cast(Torpedoes, self.torpedoes))

        for torpedoDud in torpedoDuds:
            self._removeTorpedoFollowers(klingonTorpedo=torpedoDud)

            firedBy: EnemyId = torpedoDud.firedBy

            shootingKlingon: Klingon = self._findFiringKlingon(klingonId=firedBy)
            if shootingKlingon is not None:
                self._messageConsole.displayMessage(f'{shootingKlingon.id} missed !!!!')
                self._placeTorpedoMiss(quadrant=quadrant, torpedoDud=torpedoDud)
                shootingKlingon.angle = 0
            torpedoDud.remove_from_sprite_lists()

    def _removeTorpedoFollowers(self, klingonTorpedo: KlingonTorpedo):

        followersToRemove: List[Sprite] = []
        for follower in self.torpedoFollowers:
            follower: KlingonTorpedoFollower = cast(KlingonTorpedoFollower, follower)
            if follower.following == klingonTorpedo.id:
                self.logger.debug(f'Removing follower: {follower.id}')
                followersToRemove.append(follower)

        for followerToRemove in followersToRemove:
            followerToRemove.remove_from_sprite_lists()

    def _findFiringKlingon(self, klingonId: EnemyId) -> Klingon:
        """

        Args:
            klingonId:

        Returns:  May return 'None' if the Enterprise killed him
        """

        fndKlingon: Klingon = cast(Klingon, None)
        for klingon in self._klingonList:
            klingon: Klingon = cast(Klingon, klingon)
            if klingon.id == klingonId:
                fndKlingon = klingon
                break

        return fndKlingon

    def _doWeHaveLineOfSight(self, quadrant: Quadrant, shooter: Klingon, endPoint: ArcadePoint) -> LineOfSightResponse:

        startingPoint: ArcadePoint = ArcadePoint(x=shooter.center_x, y=shooter.center_y)

        obstacles: SpriteList = SpriteList()

        if quadrant.hasPlanet is True:
            obstacles.append(quadrant.planet)

        otherKlingons: Enemies = self.__buildEligibleKlingonObstacles(shooter=shooter, klingons=quadrant.klingons)

        obstacles.extend(otherKlingons)

        results: LineOfSightResponse = self._hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.debug(f'{results=}')

        return results

    def _placeTorpedoMiss(self, quadrant: Quadrant, torpedoDud: KlingonTorpedo):

        miss: KlingonTorpedoMiss = KlingonTorpedoMiss(placedTime=self._gameEngine.gameClock)

        self._placeMiss(quadrant=quadrant, torpedoDud=torpedoDud, miss=miss)
        self._misses.append(miss)

    def _loadSounds(self):

        self._soundKlingonTorpedo    = self._loadSound(bareFileName='klingonTorpedo.wav')
        self._soundShieldHit         = self._loadSound(bareFileName='ShieldHit.wav')
        self._soundKlingonCannotFire = self._loadSound(bareFileName='KlingonCannotFire.wav')

    def __fireKlingonTorpedo(self, klingon: Klingon, enterprise: Enterprise):

        self.logger.debug(f'Klingon @ {klingon.gameCoordinates} firing; Enterprise @ {enterprise.gameCoordinates}')
        self._messageConsole.displayMessage(f'Klingon @ {klingon.gameCoordinates} firing; Enterprise @ {enterprise.gameCoordinates}')
        #
        # Use the enterprise arcade position rather than compute the sector center;  That way we
        # can use Arcade collision detection
        #
        klingonPoint:    ArcadePoint = ArcadePoint(x=klingon.center_x, y=klingon.center_y)
        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)

        klingonTorpedo: KlingonTorpedo = KlingonTorpedo()
        klingonTorpedo.center_x = klingonPoint.x
        klingonTorpedo.center_y = klingonPoint.y
        klingonTorpedo.inMotion = True
        klingonTorpedo.destinationPoint  = enterprisePoint
        klingonTorpedo.firedFromPosition = klingon.gameCoordinates
        klingonTorpedo.firedBy           = klingon.id
        klingonTorpedo.followers         = self.torpedoFollowers

        self.torpedoes.append(klingonTorpedo)
        self._soundKlingonTorpedo.play(volume=self._gameSettings.soundVolume.value)
        self.logger.info(f'{klingonTorpedo.firedFromPosition=}')

    def __pointAtEnterprise(self, klingon: Klingon, enterprise: Enterprise):

        currentPoint:     ArcadePoint = ArcadePoint(x=klingon.center_x, y=klingon.center_y)
        destinationPoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)

        normalAngle: float = self._computer.computeAngleToTarget(shooter=currentPoint, deadMeat=destinationPoint)
        klingon.angle = normalAngle + 125

        self.logger.debug(f'{klingon.angle=}')

    def __buildEligibleKlingonObstacles(self, shooter: Klingon, klingons: Enemies) -> Enemies:
        """

        Returns:  A list of klingons excluding the shooter
        """
        obstacles: Enemies = Enemies([])
        for klingon in klingons:
            if klingon.id != shooter.id:
                obstacles.append(klingon)
        return obstacles
