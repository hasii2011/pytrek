
from logging import Logger
from logging import getLogger

from math import atan2
from math import sin
from math import fabs
from math import sqrt

from random import choice

from pytrek.engine.Computer import Computer
from pytrek.engine.Direction import Direction
from pytrek.engine.DirectionData import DirectionData
from pytrek.engine.PlayerType import PlayerType
from pytrek.engine.devices.DeviceStatus import DeviceStatus
from pytrek.engine.devices.DeviceType import DeviceType
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.ShieldHitData import ShieldHitData
from pytrek.engine.ShipCondition import ShipCondition

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.commander.Commander import Commander
from pytrek.gui.gamepieces.klingon.Klingon import Klingon
from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander

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
        self._gameState.remainingKlingons        = self._gameState.remainingKlingons - self._gameState.remainingCommanders

        playerType: PlayerType = self._gameState.playerType
        # Novice and Fair players do not get Super Commanders
        if playerType != PlayerType.Novice and playerType != PlayerType.Fair:
            self._gameState.remainingSuperCommanders = self._intelligence.generateInitialSuperCommanderCount(self._gameState.remainingKlingons)

            # Adjust total Klingons by # of super commanders
            self._gameState.remainingKlingons = self._gameState.remainingKlingons - self._gameState.remainingSuperCommanders
        else:
            self._gameState.remainingSuperCommanders = 0
        self._accumulatedDelta: float = 0.0
        self._gameClock:        float = 0.0

    @property
    def gameClock(self) -> float:
        """
        Read only property

        Returns:    The current real time since the game started (milliseconds)
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

    # noinspection SpellCheckingInspection
    def computeEnergyWhenBlocked(self, startSector: Coordinates, endSector: Coordinates) -> float:
        """
        C code:
        Time = dist/0.095;
        stopegy = 50.0*dist/Time

        Java:
            power = 20.0 + 100.0*game.dist;
            game.energy -= power;


        Returns:   The Java calculated version

        """
        travelDistance: float = self._computer.computeQuadrantDistance(startSector=startSector, endSector=endSector)
        elapsedTime:    float = travelDistance / 0.095

        self.logger.info(f'{travelDistance=}  {elapsedTime=}')
        self._gameState.opTime = elapsedTime

        # stopEnergy: float = 50.0 * travelDistance / elapsedTime
        stopEnergy: float = 20.0 + 100.0 * travelDistance

        return stopEnergy

    # noinspection SpellCheckingInspection
    def computeShieldHit(self, torpedoHit: float) -> ShieldHitData:
        """
        ```
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
        ```
        Returns: Computed shield hit data
        """
        changeFactor:       float = 0.25 + (0.5 * self._intelligence.rand())
        proportionalFactor: float = 1.0 / DEFAULT_FULL_SHIELDS
        proportion:         float = proportionalFactor * self._gameState.shieldEnergy

        if proportion < 0.1:
            proportion = 0.1
        shieldHit: float = proportion * changeFactor * torpedoHit + 1.0

        shieldAbsorptionValue:   float = 0.8 * shieldHit
        degradedTorpedoHitValue: float = torpedoHit - shieldHit

        shieldHitData: ShieldHitData = ShieldHitData(shieldAbsorptionValue=shieldAbsorptionValue, degradedTorpedoHitValue=degradedTorpedoHitValue)

        return shieldHitData

    # noinspection SpellCheckingInspection
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

    def computeCloseCoordinates(self, targetCoordinates: Coordinates) -> DirectionData:
        """

        Args:
            targetCoordinates:  The location occupied by an object that we bumped up against

        Returns:  Coordinates somewhere around the target we bumped

        """
        x: int = targetCoordinates.x
        y: int = targetCoordinates.y
        newX: int = 0
        newY: int = 0
        direction: Direction = self.randomDirection()
        if direction == Direction.North:
            newX = x
            newY = y - 1
        elif direction == Direction.South:
            newX = x
            newY = y + 1
        elif direction == Direction.East:
            newX = x + 1
            newY = y
        elif direction == Direction.West:
            newX = x - 1
            newY = y
        elif direction == Direction.NorthEast:
            newX = x + 1
            newY = y - 1
        elif direction == Direction.SouthEast:
            newX = x + 1
            newY = y + 1
        elif direction == Direction.NorthWest:
            newX = x - 1
            newY = y - 1
        elif direction == Direction.SouthWest:
            newX = x - 1
            newY = y + 1

        closeCoordinates: Coordinates = Coordinates(x=newX, y=newY)

        directionData: DirectionData = DirectionData(coordinates=closeCoordinates, direction=direction)

        return directionData

    def randomDirection(self) -> Direction:
        """"""
        return choice(list(Direction))

    def doPhasers(self, distance: float, enemyPower: float, powerAmount: float):
        # noinspection SpellCheckingInspection
        """
        This codes does a single hit at a time

        Caller should check to make sure there is an enemy at the target coordinates
        Caller should indicate via console message that we are locked on target

        ```java
            hits[i] = fabs(game.kpower[i])/(PHASEFAC*pow(0.90,game.kdist[i]));

           over = (0.01 + 0.05*tk.rand())*hits[i];
           temp = powrem;
           powrem -= hits[i] + over;
           if (powrem <= 0 && temp < hits[i]) hits[i] = temp;
           if (powrem <= 0) over = 0.0;
           extra += over;
           bursts [i] = hits [i] + over;
        ```
        Args:
            distance:       sector distance between enterprise and enemy we are shooting at
            enemyPower:     The enemy's power reserve
            powerAmount:    The amount of power to expend
        Returns:
        """
        phaserBurstToTerminate: float = self._gameSettings.phaserBurstToTerminate

        rPow:   float = powerAmount
        powRem: float = rPow

        if enemyPower <= phaserBurstToTerminate:
            hit: float = phaserBurstToTerminate
        else:
            phaserFactor: float = self._gameSettings.phaserFactor

            hit = fabs(enemyPower / phaserFactor * pow(0.90, distance))
            over: float = (0.01 + 0.05 * self._intelligence.rand()) * hit

            temp: float = powRem

            powRem = hit + over
            if powRem <= 0 and temp < hit:
                hit = temp

        return hit

    def hitThem(self, distance: float, hit: float, enemyPower: float) -> float:
        # noinspection SpellCheckingInspection
        """
        Register phaser hit on enemy

        ```c
            dustfac = 0.9 + 0.01*Rand();
            hit = wham*pow(dustfac,kdist[kk]);
            kpini = kpower[kk];
            kp = fabs(kpini);
            if (phasefac*hit < kp) kp = phasefac*hit;
            kpower[kk] -= (kpower[kk] < 0 ? -kp: kp);
            kpow = kpower[kk];
        ```
        Args:
            distance:   sector distance between enterprise and enemy we are shooting at
            hit:        Hit to apply to enemy
            enemyPower: The power the enemy we want to hurt currently has

        Returns:  The power drain to apply to the enemy
        """

        phaserFactor: float = self._gameSettings.phaserFactor

        wham:       float = hit
        dustFactor: float = 0.8 + 0.01 * self._intelligence.rand()

        damage: float = wham * pow(dustFactor, distance)

        kpInit: float = enemyPower
        kp:     float = fabs(kpInit)
        if phaserFactor * damage < kp:
            kp = phaserFactor * damage

        return kp

    def decrementEnemyCount(self, enemy: Enemy):
        """
        Decrements the appropriate counter
        Args:
            enemy:  The enemy we just whacked
        """

        if isinstance(enemy, Klingon) is True:
            self._gameState.remainingKlingons -= 1
        elif isinstance(enemy, Commander) is True:
            self._gameState.remainingCommanders -= 1
        elif isinstance(enemy, SuperCommander):
            self._gameState.remainingSuperCommanders -= 1
