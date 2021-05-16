
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import Sprite
from arcade import SpriteList
from arcade import check_for_collision_with_list

from pytrek.Constants import SOUND_VOLUME_HIGH
from pytrek.GameState import GameState
from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.engine.Computer import Computer
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.ShieldHitData import ShieldHitData
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import KlingonId

from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.gui.gamepieces.KlingonTorpedo import KlingonTorpedo
from pytrek.gui.gamepieces.KlingonTorpedoFollower import KlingonTorpedoFollower

from pytrek.model.Quadrant import Quadrant


class KlingonTorpedoHandler:

    KLINGON_TORPEDO_EVENT_SECONDS = 10      # TODO  Compute this

    IMAGE_ROTATION: int = 90  # Image might not be lined up right, set this to offset

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._gameEngine:   GameEngine   = GameEngine()
        self._gameState:    GameState    = GameState()
        self._computer:     Computer     = Computer()
        self._intelligence: Intelligence = Intelligence()
        self._devices:      Devices      = Devices()

        self._klingonTorpedoes: SpriteList = cast(SpriteList, None)
        self._torpedoFollowers: SpriteList = cast(SpriteList, None)

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='klingon_torpedo.wav')
        self._soundKlingonTorpedo: Sound = Sound(file_name=fqFileName)

        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='ShieldHit.wav')

        self._soundShieldHit: Sound = Sound(file_name=fqFileName)

        self._lastTimeCheck: float = self._gameEngine.gameClock / 1000
        self.logger.info(f'{self._lastTimeCheck=}')

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
    def klingonList(self) -> SpriteList:
        return self._klingonList

    @klingonList.setter
    def klingonList(self, newValues: SpriteList):
        self._klingonList = newValues

    def fireTorpedoesAtEnterpriseIfNecessary(self, quadrant: Quadrant):

        currentTime:    float = self._gameEngine.gameClock
        deltaClockTime: float = currentTime - self._lastTimeCheck
        if deltaClockTime > KlingonTorpedoHandler.KLINGON_TORPEDO_EVENT_SECONDS:
            self.logger.info(f'Time for Klingons to fire torpedoes')
            klingons: List[Klingon] = quadrant.klingons
            for klingon in klingons:
                self._pointAtEnterprise(klingon=klingon, enterprise=quadrant.enterprise)

                self._fireKlingonTorpedo(klingon=klingon, enterprise=quadrant.enterprise)

            self._lastTimeCheck = currentTime

    def handleKlingonTorpedoHits(self, quadrant: Quadrant):
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
            self.logger.info(f'{expendedTorpedo.uuid} arrived at destination')
            self._removeTorpedoFollowers(klingonTorpedo=expendedTorpedo)

            firedBy: KlingonId = expendedTorpedo.firedBy
            shootingKlingon: Klingon = self._findFiringKlingon(klingonId=firedBy)

            shootingKlingon.angle = 0
            hitValue: float = self._computer.computeHitValueOnEnterprise(klingonPosition=shootingKlingon.currentPosition,
                                                                         enterprisePosition=quadrant.enterpriseCoordinates,
                                                                         klingonPower=shootingKlingon.power)
            expendedTorpedo.remove_from_sprite_lists()

            self.logger.debug(f"Original Hit Value: {hitValue:4f} {shootingKlingon=}")

            if self._devices.getDeviceStatus(DeviceType.Shields) == DeviceStatus.Up:
                shieldHitData: ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=hitValue)
            else:
                shieldHitData: ShieldHitData = ShieldHitData(degradedTorpedoHitValue=hitValue, shieldAbsorptionValue=0.0)

            shieldAbsorptionValue   = shieldHitData.shieldAbsorptionValue
            degradedTorpedoHitValue = shieldHitData.degradedTorpedoHitValue

            # self.messageConsole.addText(f"Shield Hit: {shieldAbsorptionValue:4f}  Enterprise hit: {degradedTorpedoHitValue:4f}")
            self._soundShieldHit.play()
            self._gameEngine.degradeShields(shieldAbsorptionValue)

            self._gameEngine.degradeEnergyLevel(shieldHitData.degradedTorpedoHitValue)
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

    def handleKlingonTorpedoMisses(self):

        torpedoDuds: List[KlingonTorpedo] = self._findTorpedoMisses()

        for torpedoDud in torpedoDuds:
            self._removeTorpedoFollowers(klingonTorpedo=torpedoDud)

            firedBy: KlingonId = torpedoDud.firedBy

            shootingKlingon: Klingon = self._findFiringKlingon(klingonId=firedBy)
            self.logger.info(f'{shootingKlingon} missed !!!!')
            torpedoDud.remove_from_sprite_lists()

    def _fireKlingonTorpedo(self, klingon: Klingon, enterprise: Enterprise):

        self.logger.info(f'Klingon @ {klingon.currentPosition} firing; Enterprise @ {enterprise.currentPosition}')

        #
        # Use the enterprise arcade position rather than compute the sector center;  That way we
        # can use Arcade collision detection
        #
        klingonPoint:    ArcadePosition = ArcadePosition(x=klingon.center_x, y=klingon.center_y)
        enterprisePoint: ArcadePosition = ArcadePosition(x=enterprise.center_x, y=enterprise.center_y)

        klingonTorpedo: KlingonTorpedo = KlingonTorpedo()
        klingonTorpedo.center_x = klingonPoint.x
        klingonTorpedo.center_y = klingonPoint.y
        klingonTorpedo.inMotion = True
        klingonTorpedo.destinationPoint  = enterprisePoint
        klingonTorpedo.firedFromPosition = klingon.currentPosition
        klingonTorpedo.firedBy           = klingon.id
        klingonTorpedo.followers         = self.torpedoFollowers

        self.klingonTorpedoes.append(klingonTorpedo)
        self._soundKlingonTorpedo.play(volume=SOUND_VOLUME_HIGH)
        self.logger.info(f'{klingonTorpedo.firedFromPosition=}')

    def _removeTorpedoFollowers(self, klingonTorpedo: KlingonTorpedo):

        followersToRemove: List[Sprite] = []
        for follower in self.torpedoFollowers:
            follower: KlingonTorpedoFollower = cast(KlingonTorpedoFollower, follower)
            if follower.following == klingonTorpedo.uuid:
                self.logger.debug(f'Removing follower: {follower.uuid}')
                followersToRemove.append(follower)

        for followerToRemove in followersToRemove:
            followerToRemove.remove_from_sprite_lists()

    def _findFiringKlingon(self, klingonId: KlingonId) -> Klingon:

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

    def _pointAtEnterprise(self, klingon: Klingon, enterprise: Enterprise):

        currentPoint:     ArcadePosition = ArcadePosition(x=klingon.center_x, y=klingon.center_y)
        destinationPoint: ArcadePosition = ArcadePosition(x=enterprise.center_x, y=enterprise.center_y)

        normalAngle: float = self._computer.computeAngleToTarget(shooter=currentPoint, deadMeat=destinationPoint)
        klingon.angle = normalAngle + 125

        self.logger.info(f'{klingon.angle=}')
