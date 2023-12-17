
from typing import cast

from logging import Logger
from logging import getLogger

from codeallybasic.Singleton import Singleton

from pytrek.engine.Intelligence import Intelligence
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.model.Coordinates import Coordinates

from pytrek.engine.PlayerType import PlayerType
from pytrek.engine.GameType import GameType
from pytrek.engine.ShipCondition import ShipCondition

from pytrek.settings.GameSettings import GameSettings


# noinspection PyAttributeOutsideInit
class GameState(Singleton):
    """
    Keeps track of the game state
    """
    def init(self):

        self.logger:  Logger       = getLogger(__name__)
        gameSettings: GameSettings = GameSettings()
        intelligence: Intelligence = Intelligence()
        playerType:   PlayerType   = gameSettings.playerType
        gameType:     GameType     = gameSettings.gameType

        self._playerType: PlayerType  = playerType
        self._gameType:     GameType  = gameType
        self._energy:       float     = gameSettings.initialEnergyLevel
        self._shieldEnergy: float     = gameSettings.initialShieldEnergy
        self._torpedoCount: int       = gameSettings.initialTorpedoCount
        self._starDate:     float     = intelligence.generateInitialStarDate()
        self._inTime:       float     = intelligence.generateInitialGameTime()
        self._opTime:       float     = 0.0

        self._remainingGameTime:   float = intelligence.generateInitialGameTime()
        self._remainingKlingons:   int   = intelligence.generateInitialKlingonCount(gameType=gameType, playerType=playerType)
        self._remainingCommanders: int   = intelligence.generateInitialCommanderCount(playerType=playerType, generatedKlingons=self._remainingKlingons)

        self._starBaseCount: int = intelligence.generateInitialStarBaseCount()
        self._planetCount:   int = intelligence.generateInitialPlanetCount()

        # Adjust total Klingon counts by # of commanders
        self._remainingKlingons = self._remainingKlingons - self._remainingCommanders

        # Novice and Fair players do not get Super Commanders
        if playerType != PlayerType.Novice and playerType != PlayerType.Fair:
            self._remainingSuperCommanders = intelligence.generateInitialSuperCommanderCount(playerType=playerType, numberOfKlingons=self._remainingKlingons)
            # Adjust total Klingons by # of super commanders
            self._remainingKlingons = self._remainingKlingons - self._remainingSuperCommanders
        else:
            self._remainingSuperCommanders = 0

        self._shipCondition:             ShipCondition  = ShipCondition.Green
        self.currentQuadrantCoordinates: Coordinates    = cast(Coordinates, None)
        self.currentSectorCoordinates:   Coordinates    = cast(Coordinates, None)

        self._enterprise: Enterprise = Enterprise()

        self.gameActive:    bool = True

        self.logger.info(f'Game State singleton initialized')

    @property
    def enterprise(self) -> Enterprise:
        return self._enterprise

    @property
    def energy(self) -> float:
        return self._energy

    @energy.setter
    def energy(self, theNewValue: float):
        self._energy = theNewValue

    @property
    def shieldEnergy(self) -> float:
        return self._shieldEnergy

    @shieldEnergy.setter
    def shieldEnergy(self, theNewValue: float):
        self._shieldEnergy = theNewValue

    @property
    def inTime(self) -> float:
        return self._inTime

    @inTime.setter
    def inTime(self, theNewValue: float):
        self._inTime = theNewValue

    @property
    def opTime(self) -> float:
        """
        Returns:    The time it took for the last operation to complete
        """
        return self._opTime

    @opTime.setter
    def opTime(self, theNewValue: float):
        self._opTime = theNewValue

    @property
    def starDate(self) -> float:
        return self._starDate

    @starDate.setter
    def starDate(self, theNewValue: float):
        self._starDate = theNewValue

    @property
    def remainingGameTime(self) -> float:
        return self._remainingGameTime

    @remainingGameTime.setter
    def remainingGameTime(self, theNewValue: float):
        self._remainingGameTime = theNewValue

    @property
    def remainingKlingons(self):
        return self._remainingKlingons

    @remainingKlingons.setter
    def remainingKlingons(self, theNewValue: int):
        self._remainingKlingons = theNewValue

    @property
    def remainingCommanders(self) -> int:
        return self._remainingCommanders

    @remainingCommanders.setter
    def remainingCommanders(self, theNewValue: int):
        self._remainingCommanders = theNewValue

    @property
    def remainingSuperCommanders(self) -> int:
        return self._remainingSuperCommanders

    @remainingSuperCommanders.setter
    def remainingSuperCommanders(self, theNewValue: int):
        self._remainingSuperCommanders = theNewValue

    @property
    def torpedoCount(self) -> int:
        return self._torpedoCount

    @torpedoCount.setter
    def torpedoCount(self, theNewValue: int):
        self._torpedoCount = theNewValue

    @property
    def shipCondition(self) -> ShipCondition:
        return self._shipCondition

    @shipCondition.setter
    def shipCondition(self, theNewValue: ShipCondition):
        self._shipCondition = theNewValue

    @property
    def playerType(self) -> PlayerType:
        return self._playerType

    @playerType.setter
    def playerType(self, theNewValue: PlayerType):
        self._playerType = theNewValue

    @property
    def gameType(self) -> GameType:
        return self._gameType

    @gameType.setter
    def gameType(self, theNewValue: GameType):
        self._gameType = theNewValue

    @property
    def currentQuadrantCoordinates(self) -> Coordinates:
        return self._currentQuadrantCoordinates

    @currentQuadrantCoordinates.setter
    def currentQuadrantCoordinates(self, theNewValue: Coordinates):
        self._currentQuadrantCoordinates = theNewValue

    @property
    def currentSectorCoordinates(self) -> Coordinates:
        return self._currentSectorCoordinates

    @currentSectorCoordinates.setter
    def currentSectorCoordinates(self, theNewValue: Coordinates):
        self._currentSectorCoordinates = theNewValue

    @property
    def starBaseCount(self) -> int:
        return self._starBaseCount

    @starBaseCount.setter
    def starBaseCount(self, newValue: int):
        self._starBaseCount = newValue

    @property
    def planetCount(self) -> int:
        return self._planetCount

    @planetCount.setter
    def planetCount(self, newValue: int):
        self._planetCount = newValue

    def resetStatistics(self):
        self.gameActive = True

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} at {hex(id(self))}>'
