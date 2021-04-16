
from typing import cast

from pytrek.Singleton import Singleton
from pytrek.model.Coordinates import Coordinates
from pytrek.engine.PlayerType import PlayerType
from pytrek.engine.GameType import GameType
from pytrek.engine.ShipCondition import ShipCondition


class GameState(Singleton):
    """
    Keeps track of the game state;  Is initialized by the Game Engine via game type, player type, and external
    settings data
    """
    def init(self):

        self._energy:              float = 0.0
        self._shieldEnergy:        float = 0.0
        self._starDate:            float = 0.0
        self._inTime:              float = 0.0
        self._opTime:              float = 0.0  # #define Time a.Time time taken by current operation
        self._remainingGameTime:   float = 0.0
        self._remainingKlingons:   int   = 0
        self._remainingCommanders: int   = 0
        self._torpedoCount:        int   = 0
        self._shipCondition:       ShipCondition = ShipCondition.Green

        self._skill:    PlayerType = cast(PlayerType, None)
        self._gameType: GameType   = cast(GameType, None)

        self.currentQuadrantCoordinates: Coordinates = cast(Coordinates, None)
        self.currentSectorCoordinates:   Coordinates = cast(Coordinates, None)

        self.gameActive:    bool = True

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
    def skill(self) -> PlayerType:
        return self._skill

    @skill.setter
    def skill(self, theNewValue: PlayerType):
        self._skill = theNewValue

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

    def resetStatistics(self):
        self.gameActive = True

    def __repr__(self):
        return f'<{self.__class__.__name__} at {hex(id(self))}>'
