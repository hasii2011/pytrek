
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import Sprite
from arcade import check_for_collision_with_list

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.ShieldHitData import ShieldHitData

from pytrek.gui.gamepieces.BaseEnemy import BaseEnemy
from pytrek.gui.gamepieces.BaseEnemy import EnemyId
from pytrek.gui.gamepieces.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.BasicMiss import BasicMiss
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemy

from pytrek.gui.gamepieces.KlingonTorpedo import KlingonTorpedo
from pytrek.gui.gamepieces.KlingonTorpedoMiss import KlingonTorpedoMiss

from pytrek.mediators.BaseMediator import Misses
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

        self._fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant, enemies=quadrant.klingons)
        self.torpedoes.update()
        self.torpedoFollowers.update()

        self._handleKlingonTorpedoHits(quadrant)
        self._handleTorpedoMisses(quadrant, enemies=quadrant.klingons)
        self._handleMissRemoval(quadrant, cast(Misses, self._misses))

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
        for sprite in expendedTorpedoes:
            expendedTorpedo: KlingonTorpedo = cast(KlingonTorpedo, sprite)
            self.logger.info(f'{expendedTorpedo.id} arrived at destination')
            self._removeTorpedoFollowers(enemyTorpedo=expendedTorpedo)

            firedBy: EnemyId = expendedTorpedo.firedBy
            shootingKlingon: BaseEnemy = self._findFiringEnemy(enemyId=firedBy, enemies=quadrant.klingons)

            if shootingKlingon is not None:
                shootingKlingon.angle = 0
                hitValue: float = self._computer.computeHitValueOnEnterprise(klingonPosition=shootingKlingon.gameCoordinates,
                                                                             enterprisePosition=quadrant.enterpriseCoordinates,
                                                                             klingonPower=shootingKlingon.power)

                self.logger.debug(f"Original Hit Value: {hitValue:.4f} {shootingKlingon=}")

                if self._devices.getDeviceStatus(DeviceType.Shields) == DeviceStatus.Up:
                    shieldHitData: ShieldHitData = self._gameEngine.computeShieldHit(torpedoHit=hitValue)
                else:
                    shieldHitData = ShieldHitData(degradedTorpedoHitValue=hitValue, shieldAbsorptionValue=0.0)
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

    def _playCannotFireSound(self):
        """
        Implement empty base class method
        """
        self._soundKlingonCannotFire.play(volume=self._gameSettings.soundVolume.value)

    def _playTorpedoFiredSound(self):
        """
        Implement empty base class method
        """
        self._soundKlingonTorpedo.play(volume=self._gameSettings.soundVolume.value)

    def _loadSounds(self):

        self._soundKlingonTorpedo    = self._loadSound(bareFileName='klingonTorpedo.wav')
        self._soundShieldHit         = self._loadSound(bareFileName='ShieldHit.wav')
        self._soundKlingonCannotFire = self._loadSound(bareFileName='KlingonCannotFire.wav')

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

        klingonTorpedo: KlingonTorpedo = KlingonTorpedo()

        klingonTorpedo.center_x = klingonPoint.x
        klingonTorpedo.center_y = klingonPoint.y
        klingonTorpedo.inMotion = True
        klingonTorpedo.destinationPoint = enterprisePoint
        klingonTorpedo.firedFromPosition = enemy.gameCoordinates
        klingonTorpedo.firedBy = enemy.id
        klingonTorpedo.followers = self.torpedoFollowers

        return klingonTorpedo

    def _getTorpedoMiss(self) -> BasicMiss:
        """
        Implement empty base class method

        Returns:  An appropriate 'miss' sprite
        """
        return KlingonTorpedoMiss(placedTime=self._gameEngine.gameClock)
