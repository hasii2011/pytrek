
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
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import Enemies
from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.gui.gamepieces.KlingonTorpedo import KlingonTorpedo
from pytrek.gui.gamepieces.KlingonTorpedoFollower import KlingonTorpedoFollower
from pytrek.gui.gamepieces.KlingonTorpedoMiss import KlingonTorpedoMiss

from pytrek.mediators.BaseMediator import BaseMediator
from pytrek.mediators.BaseMediator import LineOfSightResponse

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant

from pytrek.Constants import DEFAULT_FULL_SHIELDS
from pytrek.Constants import SOUND_VOLUME_HIGH

from pytrek.LocateResources import LocateResources


class KlingonTorpedoMediator(BaseMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__()

        self._devices: Devices = Devices()

        self._klingonTorpedoes: SpriteList = SpriteList()
        self._torpedoFollowers: SpriteList = SpriteList(is_static=True)
        self._torpedoDuds:      SpriteList = SpriteList()

        self._loadSounds()

        self._lastTimeCheck: float = self._gameEngine.gameClock / 1000
        self.logger.info(f'{self._lastTimeCheck=}')

    def draw(self):

        self.klingonTorpedoes.draw()
        self.torpedoFollowers.draw()
        self.torpedoDuds.draw()

    def update(self, quadrant: Quadrant):

        self._fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant)
        self.klingonTorpedoes.update()
        self.torpedoFollowers.update()

        self._handleKlingonTorpedoHits(quadrant)
        self._handleKlingonTorpedoMisses()
        self._handleDudRemoval()

    @property
    def klingonTorpedoes(self) -> SpriteList:
        return self._klingonTorpedoes

    @klingonTorpedoes.setter
    def klingonTorpedoes(self, newList: SpriteList):
        """
        Args:
            newList:
        """
        self._klingonTorpedoes = newList

    @property
    def torpedoFollowers(self) -> SpriteList:
        return self._torpedoFollowers

    @torpedoFollowers.setter
    def torpedoFollowers(self, newValues: SpriteList):
        self._torpedoFollowers = newValues

    @property
    def torpedoDuds(self) -> SpriteList:
        return self._torpedoDuds

    @torpedoDuds.setter
    def torpedoDuds(self, newValues: SpriteList):
        self._torpedoDuds = newValues

    @property
    def klingonList(self) -> SpriteList:
        return self._klingonList

    @klingonList.setter
    def klingonList(self, newValues: SpriteList):
        self._klingonList = newValues

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
                    self._soundKlingonCannotFire.play(volume=SOUND_VOLUME_HIGH)
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

        expendedTorpedoes: List[Sprite] = check_for_collision_with_list(sprite=quadrant.enterprise, sprite_list=self.klingonTorpedoes)
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

                self._messageConsole.displayMessage(f"Shields at {shieldPercentage} percent.  Enterprise energy degraded by: {degradedTorpedoHitValue:.2f}")

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

    def _handleKlingonTorpedoMisses(self):

        torpedoDuds: List[KlingonTorpedo] = self._findTorpedoMisses()

        for torpedoDud in torpedoDuds:
            self._removeTorpedoFollowers(klingonTorpedo=torpedoDud)

            firedBy: EnemyId = torpedoDud.firedBy

            shootingKlingon: Klingon = self._findFiringKlingon(klingonId=firedBy)
            if shootingKlingon is not None:
                self._messageConsole.displayMessage(f'{shootingKlingon.id} missed !!!!')
                self.__placeTorpedoDud(torpedoDud=torpedoDud)
                shootingKlingon.angle = 0
            torpedoDud.remove_from_sprite_lists()

    def _removeTorpedoFollowers(self, klingonTorpedo: KlingonTorpedo):

        followersToRemove: List[Sprite] = []
        for follower in self.torpedoFollowers:
            follower: KlingonTorpedoFollower = cast(KlingonTorpedoFollower, follower)
            if follower.following == klingonTorpedo.id:
                self.logger.debug(f'Removing follower: {follower.uuid}')
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

    def _findTorpedoMisses(self):

        torpedoDuds: List[KlingonTorpedo] = []
        for torpedo in self.klingonTorpedoes:
            torpedo: KlingonTorpedo = cast(KlingonTorpedo, torpedo)
            if torpedo.inMotion is False:
                torpedoDuds.append(torpedo)
        return torpedoDuds

    def _doWeHaveLineOfSight(self, quadrant: Quadrant, shooter: Klingon, endPoint: ArcadePoint) -> LineOfSightResponse:

        startingPoint: ArcadePoint = ArcadePoint(x=shooter.center_x, y=shooter.center_y)

        obstacles: SpriteList = SpriteList()

        if quadrant.hasPlanet is True:
            obstacles.append(quadrant._planet)
        otherKlingons: Enemies = self.__buildEligibleKlingonObstacles(shooter=shooter, klingons=quadrant.klingons)

        obstacles.extend(otherKlingons)

        results: LineOfSightResponse = self.hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.info(f'{results=}')

        return results

    def _loadSounds(self):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='klingonTorpedo.wav')
        self._soundKlingonTorpedo: Sound = Sound(file_name=fqFileName)
        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='ShieldHit.wav')
        self._soundShieldHit: Sound = Sound(file_name=fqFileName)

        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='KlingonCannotFire.wav')

        self._soundKlingonCannotFire: Sound = Sound(file_name=fqFileName)

    def _handleDudRemoval(self):

        duds:            SpriteList = self._torpedoDuds
        currentTime:     float = self._gameEngine.gameClock
        displayInterval: int   = self._gameSettings.basicMissDisplayInterval

        for dud in duds:
            dud: KlingonTorpedoMiss = cast(KlingonTorpedoMiss, dud)
            deltaTime: float = currentTime - dud.placedTime
            if deltaTime >= displayInterval:
                dud.remove_from_sprite_lists()

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

        self.klingonTorpedoes.append(klingonTorpedo)
        self._soundKlingonTorpedo.play(volume=SOUND_VOLUME_HIGH)
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

    def __placeTorpedoDud(self, torpedoDud: KlingonTorpedo):

        dud: KlingonTorpedoMiss = KlingonTorpedoMiss(placedTime=self._gameEngine.gameClock)

        # Convert to game coordinates
        # Then to game point in order to get dud to center in sector
        gameCoordinates: Coordinates = self._computer.computeSectorCoordinates(x=torpedoDud.center_x, y=torpedoDud.center_y)
        arcadePoint:     ArcadePoint = GamePiece.gamePositionToScreenPosition(gameCoordinates=gameCoordinates)

        dud.center_x = arcadePoint.x
        dud.center_y = arcadePoint.y

        self.logger.info(f'Placed dud at: {gameCoordinates=}  {arcadePoint=}')
        self._torpedoDuds.append(dud)
