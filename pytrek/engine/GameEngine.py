
from logging import Logger
from logging import getLogger

from pytrek.GameState import GameState
from pytrek.Singleton import Singleton
from pytrek.engine.Intelligence import Intelligence
from pytrek.settings.GameSettings import GameSettings


class GameEngine(Singleton):

    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        self._gameState:    GameState    = GameState()
        self._gameSettings: GameSettings = GameSettings()
        self._intelligence: Intelligence = Intelligence()

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
