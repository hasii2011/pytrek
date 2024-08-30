
from typing import cast

from logging import Logger
from logging import getLogger

from codeallybasic.SingletonV3 import SingletonV3

from pytrek.Constants import MINIMUM_SAFE_WARP_FACTOR
from pytrek.GameState import GameState

from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.gui.MessageConsoleProxy import MessageConsoleProxy

from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.settings.GameSettings import GameSettings


class GalaxyMediator(metaclass=SingletonV3):
    """
    This class aids in updating the Galaxy model and the game state
    """

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._computer:     Computer     = Computer()
        self._gameState:    GameState    = GameState()
        self._gameSettings: GameSettings = GameSettings()
        self._gameEngine:   GameEngine   = GameEngine()
        self._galaxy:       Galaxy       = Galaxy()
        self._intelligence: Intelligence = Intelligence()

        self._messageConsoleProxy: MessageConsoleProxy = MessageConsoleProxy()
        assert self._messageConsoleProxy.initialized is True, 'The console proxy should have set up at game startup'

    def doWarp(self, currentCoordinates: Coordinates, destinationCoordinates: Coordinates):
        """
        This actually moves the Enterprise and updates the Game State

        Args:
            currentCoordinates:     Where we were
            destinationCoordinates: Where we want to go
        """
        finalDestinationCoordinates: Coordinates = destinationCoordinates
        warpFactor:                  float = self._gameState.warpFactor
        travelDistance:              float = self._computer.computeGalacticDistance(startQuadrantCoordinates=currentCoordinates, endQuadrantCoordinates=destinationCoordinates)

        if warpFactor > MINIMUM_SAFE_WARP_FACTOR:
            #
            # See if we damaged our engines
            #
            if self._intelligence.determineIfWarpEngineAreDamaged(warpFactor=warpFactor, distance=travelDistance) is True:
                self._damageTheEngines()
                damagedTravelDistance:  float       = self._intelligence.randomFloat() * travelDistance
                direction:              float       = self._computer.computeGameTravelDirection(startCoordinates=currentCoordinates, endCoordinates=destinationCoordinates)
                #
                scaledDistance:         float       = travelDistance / Computer.SCALE_DOWN_FACTOR
                # .computeDestinationCoordinates is regular math so used 'normal' x, y
                finalDestinationCoordinates = self._computer.computeDestinationCoordinates(startCoordinates=currentCoordinates, angle=direction, distance=scaledDistance)
                #
                # Make adjustments so regular code works
                #
                travelDistance = damagedTravelDistance

                self._messageConsoleProxy.displayMessage(f'Engineering to bridge - -')
                self._messageConsoleProxy.displayMessage(f'  Scott here.  The warp engines were damaged.')
                self._messageConsoleProxy.displayMessage(f'  We`ll have to reduce speed to warp 4.')
                self._gameState.warpFactor = 4

        #
        energyConsumed: float = self._gameEngine.computeEnergyForWarpTravel(travelDistance=travelDistance, warpFactor=warpFactor)
        self._gameState.energy -= energyConsumed
        self._gameEngine.updateTimeAfterWarpTravel(travelDistance=travelDistance, warpFactor=warpFactor)

        self.logger.info(f'After warp travel consumed energy: {energyConsumed:.2f}')

        currentQuadrant: Quadrant = self._galaxy.getQuadrant(quadrantCoordinates=currentCoordinates)

        sectorCoordinates: Coordinates = currentQuadrant.enterpriseCoordinates
        oldSector:         Sector      = currentQuadrant.getSector(sectorCoordinates=sectorCoordinates)

        oldSector.type   = SectorType.EMPTY
        oldSector.sprite = cast(GamePiece, None)
        #
        # Set up new quadrant
        #
        destinationQuadrant                        = self._galaxy.getQuadrant(quadrantCoordinates=finalDestinationCoordinates)
        self._galaxy.currentQuadrant               = destinationQuadrant
        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        self._messageConsoleProxy.displayMessage(f"Warped to: {finalDestinationCoordinates} at warp: {self._gameState.warpFactor}")

    def _determineHowFarWeGot(self):
        pass

    def _damageTheEngines(self):
        # noinspection SpellCheckingInspection
        """
        damfac = 0.5 * skill;
        damage[DWARPEN] = damfac*(3.0*Rand()+1.0);

        """
        from pytrek.engine.devices.Devices import Devices
        from pytrek.engine.devices.DeviceType import DeviceType

        damageFactor: float = self._gameSettings.damageAdjuster * self._gameState.playerType.value

        warpEngineDamageValue: float = damageFactor * (3.0 * self._intelligence.rand() + 1.0)
        devices: Devices = Devices()

        devices.setDeviceDamage(deviceType=DeviceType.WarpEngines, damageValue=warpEngineDamageValue)
