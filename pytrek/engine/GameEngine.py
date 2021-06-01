
from logging import Logger
from logging import getLogger

from math import atan2
from math import sin
from math import fabs
from math import sqrt

from pytrek.engine.Computer import Computer
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.ShieldHitData import ShieldHitData
from pytrek.engine.ShipCondition import ShipCondition

from pytrek.gui.gamepieces.Enterprise import Enterprise

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings

from pytrek.Constants import DEFAULT_FULL_SHIELDS

from pytrek.GameState import GameState
from pytrek.Singleton import Singleton


class GameEngine(Singleton):

    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        self._gameState:    GameState    = GameState()
        self._gameSettings: GameSettings = GameSettings()
        self._intelligence: Intelligence = Intelligence()
        self._computer:     Computer     = Computer()
        self._devices:      Devices      = Devices()

        self._gameState.playerType      = self._gameSettings.playerType
        self._gameState.gameType        = self._gameSettings.gameType
        self._gameState.energy          = self._gameSettings.initialEnergyLevel
        self._gameState.shieldEnergy    = self._gameSettings.initialShieldEnergy
        self._gameState.torpedoCount    = self._gameSettings.initialTorpedoCount
        self._gameState.inTime          = self._intelligence.generateInitialGameTime()
        self._gameState.shipCondition   = ShipCondition.Green
        self._gameState.opTime          = 0.0

        self._gameState.starDate          = self._intelligence.generateInitialStarDate()
        self._gameState.remainingGameTime = self._intelligence.generateInitialGameTime()
        self._gameState.remainingKlingons   = self._intelligence.generateInitialKlingonCount()
        self._gameState.remainingCommanders = self._intelligence.generateInitialCommanderCount(self._gameState.remainingKlingons)

        # Adjust total Klingon count by # of commanders
        self._gameState.remainingKlingons = self._gameState.remainingKlingons - self._gameState.remainingCommanders

        self._accumulatedDelta: float = 0.0
        self._gameClock:        float = 0.0

    @property
    def gameClock(self) -> float:
        """
        Read only property

        Returns:    The current real time since the game started (msecs)
        """
        return self._gameClock

    def impulse(self, newCoordinates: Coordinates, quadrant: Quadrant, enterprise: Enterprise):
        """

        Args:
            newCoordinates: The new sector coordinates
            quadrant:       The current quadrant travel was in
            enterprise:     The enterprise sprite
        """

        travelDistance: float = self._computer.computeQuadrantDistance(self._gameState.currentSectorCoordinates, newCoordinates)
        quadrant.placeEnterprise(enterprise, newCoordinates)

        self._gameState.currentSectorCoordinates = newCoordinates

        self.updateTimeAfterImpulseTravel(travelDistance=travelDistance)

        if self._gameState.energy < self._gameSettings.minimumImpulseEnergy:
            neededEnergyForImpulseMove = self._gameState.energy
        else:
            neededEnergyForImpulseMove = self.computeEnergyForQuadrantTravel(travelDistance=travelDistance)

        self._gameState.energy = self._gameState.energy - neededEnergyForImpulseMove

    def updateTimeAfterImpulseTravel(self, travelDistance: float):
        """
        Time = dist/0.095;

        Args:
            travelDistance:

        """
        elapsedTime = travelDistance / 0.095
        self._gameState.opTime = elapsedTime
        # self.eventEngine.fixDevices()
        self.updateTime(elapsedTime=elapsedTime)

    def updateTime(self, elapsedTime: float):
        """
        oldTime      = self.stats.remainingGameTime
        oldStarDate  = self.stats.starDate

        Args:
            elapsedTime:
        """
        self._gameState.starDate          = self._gameState.starDate + elapsedTime
        self._gameState.remainingGameTime = self._gameState.remainingGameTime - elapsedTime

    def computeEnergyForQuadrantTravel(self, travelDistance: float) -> float:
        """
        power = 20.0 + 100.0*dist;

        Args:
            travelDistance:  How far we travelled in the quadrant

        Returns: The energy necessary to do inter-quadrant travel

        """
        quadrantEnergy: float = 20 + (100.0 * travelDistance)

        self.logger.debug(f"theTravelDistance: '{travelDistance}' quadrantEnergy : '{quadrantEnergy}'")

        return quadrantEnergy

    def computeShieldHit(self, torpedoHit: float) -> ShieldHitData:
        """

        pfac = 1.0/inshld;

        # shields will take hits
        double absorb, hitsh, propor = pfac*shield;

        if(propor < 0.1)
            propor = 0.1;
        hitsh = propor*chgfac*hit+1.0;
        atackd=1;
        absorb = 0.8*hitsh;
        if (absorb > shield)
            absorb = shield;
        shield -= absorb;
        hit -= hitsh;

        Returns: Computed shield hit data
        """
        changeFactor:       float = 0.25 + (0.5 * self._intelligence.rand())
        proportionalFactor: float = 1.0 / DEFAULT_FULL_SHIELDS
        proportion:         float = proportionalFactor * self._gameState.shieldEnergy

        if proportion < 0.1:
            proportion = 0.1
        shieldHit: float = proportion * changeFactor * torpedoHit + 1.0

        shieldAbsorptionValue: float = 0.8 * shieldHit
        torpedoHit:            float = torpedoHit - shieldHit

        shieldHitData: ShieldHitData = ShieldHitData(shieldAbsorptionValue=shieldAbsorptionValue, degradedTorpedoHitValue=torpedoHit)

        return shieldHitData

    def computeHit(self, shooterPosition: Coordinates, targetPosition: Coordinates, klingonPower: float) -> float:
        """
         StarTrekScreen: Yowzah!  A dirty rotten Klingon at (7,7) took a shot at me (3,7)

        jx,jy is section position of shooter
        sectx,secty is section position of what we hit

        r = (Rand()+Rand())*0.5 -0.5;
        r += 0.002*kpower[l]*r;

        double course = 1.90985 * atan2((double)secty-jy, (double)jx-sectx);
        double ac = course + 0.25*r;
        double angle = (15.0-ac)*0.5235988;
        double bullseye = (15.0 - course)*0.5235988;

        inx,iny is sector position of thing we hit

        *hit = 700.0 + 100.0*Rand() - 1000.0*sqrt(square(ix-inx)+square(iy-iny)) * fabs(sin(bullseye-angle));
        *hit = fabs(*hit);

        Returns:

        """
        r: float = (self._intelligence.rand() + self._intelligence.rand()) * 0.5 - 0.5

        r += 0.002 * klingonPower * r
        self.logger.debug(f"{r=}")

        jx = shooterPosition.x
        jy = shooterPosition.y

        sectx = targetPosition.x
        secty = targetPosition.y

        rads = atan2(secty-jy, jx-sectx)
        self.logger.debug(f" (jx,jy): ({jx}, {jy}), (sectx,secty): ({sectx},{secty}) - rads: {rads}")

        course: float = (1.90985 * rads) + (0.25 * r)
        self.logger.debug(f"{course=}")

        ac: float = course + 0.25 * r

        angle:    float = (15.0-ac) * 0.5235988
        bullseye: float = (15.0 - course)*0.5235988

        self.logger.debug(f"{angle=} {bullseye=}")

        inx = targetPosition.x
        iny = targetPosition.y
        ix  = shooterPosition.x
        iy  = shooterPosition.y

        def square(num) -> float:
            return num * num

        hit = 700.0 + (100.0 * self._intelligence.rand()) - \
            (1000.0 * sqrt(square(ix-inx) + square(iy-iny))) * fabs(sin(bullseye-angle))

        return hit

    def degradeEnergyLevel(self, degradedTorpedoValue: float):
        """
        printf("Hit %g energy %g\n", hit, energy);
        energy -= hit;

        Args:
            degradedTorpedoValue: Value of torpedo hit after accounting for
            the hit on the shield
        """
        self._gameState.energy -= degradedTorpedoValue
        self.logger.info(f"Degraded energy level: {self._gameState.energy:.4f}")
        if self._gameState.energy < 0:
            self._gameState.energy = 0

    def degradeShields(self, shieldAbsorptionValue: float):

        if shieldAbsorptionValue > self._gameState.shieldEnergy:
            shieldAbsorptionValue = self._gameState.shieldEnergy
        self._gameState.shieldEnergy -= shieldAbsorptionValue
        if self._gameState.shieldEnergy < 0:
            self._gameState.shieldEnergy = 0
            self._devices.getDevice(DeviceType.Shields).setDeviceStatus(DeviceStatus.Down)

    def updateRealTimeClock(self, deltaTime: float):
        """

        Args:
            deltaTime:  Diff in time since last time this method was called
        """
        self._accumulatedDelta += deltaTime

        if self._accumulatedDelta > 1.0:
            self._gameClock += self._accumulatedDelta
            self._accumulatedDelta = 0.0
            self.logger.debug(f'Game Clock: {self._gameClock:.3f}')
