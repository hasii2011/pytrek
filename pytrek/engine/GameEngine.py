
from logging import Logger
from logging import getLogger

from pytrek.GameState import GameState
from pytrek.Singleton import Singleton
from pytrek.engine.Computer import Computer
from pytrek.engine.Intelligence import Intelligence
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.settings.GameSettings import GameSettings


class GameEngine(Singleton):

    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        self._gameState:    GameState    = GameState()
        self._gameSettings: GameSettings = GameSettings()
        self._intelligence: Intelligence = Intelligence()
        self._computer:     Computer     = Computer()

        self._gameState.playerType        = self._gameSettings.playerType
        self._gameState.gameType          = self._gameSettings.gameType

        self._gameState.remainingGameTime = self._intelligence.generateInitialGameTime()
        self._gameState.remainingKlingons = self._intelligence.generateInitialKlingonCount(remainingGameTime=self._gameState.remainingGameTime)

        # self.stats.energy       = self.settings.initialEnergyLevel
        # self.stats.shieldEnergy = self.settings.initialShieldEnergy
        # self.stats.torpedoCount = self.settings.initialTorpedoCount
        #
        # self.stats.intime              = self.intelligence.getInitialGameTime()
        # self.stats.shipCondition       = ShipCondition.Green
        # self.stats.opTime              = 0.0
        # self.stats.starDate            = self.intelligence.getInitialStarDate()
        # self.stats.remainingGameTime   = self.intelligence.getInitialGameTime()

        # self.stats.remainingCommanders = self.intelligence.getInitialCommanderCount()

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
