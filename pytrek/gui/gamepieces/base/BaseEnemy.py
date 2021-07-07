
from typing import NewType
from typing import cast

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion
from pytrek.model.Coordinates import Coordinates


EnemyId = NewType('EnemyId', str)


class BaseEnemy(GamePiece, SmoothMotion):

    NEVER_MOVE_INTERVAL: int = 9999
    NEVER_FIRE_INTERVAL: int = 9999

    def __init__(self, filename: str, coordinates: Coordinates, moveInterval: int = NEVER_MOVE_INTERVAL, scale: float = 1.0):

        GamePiece.__init__(self, filename=filename, scale=scale)
        SmoothMotion.__init__(self)

        self.gameCoordinates = coordinates

        self._moveInterval: int     = moveInterval

        self._id:                EnemyId = EnemyId('IdNotSet')
        self._power:             float   = cast(float, None)
        self._firingInterval:    int     = BaseEnemy.NEVER_FIRE_INTERVAL
        self._lastTimeCheck:     int     = 0
        self._timeSinceMovement: float   = 0.0

    @property
    def id(self) -> EnemyId:
        return self._id

    @id.setter
    def id(self, newValue: EnemyId):
        self._id = newValue

    @property
    def power(self) -> float:
        return self._power

    @power.setter
    def power(self, theNewValue: float):
        self._power = theNewValue

    @property
    def moveInterval(self) -> int:
        return self._moveInterval

    @moveInterval.setter
    def moveInterval(self, newValue: int):
        self._moveInterval = newValue

    @property
    def firingInterval(self) -> int:
        return self._firingInterval

    @firingInterval.setter
    def firingInterval(self, newValue: int):
        self._firingInterval = newValue

    @property
    def lastTimeCheck(self) -> int:
        """

        Returns:  Time since we last fired torpedoes
        """
        return self._lastTimeCheck

    @lastTimeCheck.setter
    def lastTimeCheck(self, newValue: int):
        self._lastTimeCheck = newValue

    @property
    def timeSinceMovement(self) -> float:
        return self._timeSinceMovement

    @timeSinceMovement.setter
    def timeSinceMovement(self, newValue: float):
        self._timeSinceMovement = newValue

    def __str__(self) -> str:
        return f'{self.id}'

    def __repr__(self) -> str:
        return f'{self.id} {self.power=} {self.firingInterval=} {self.moveInterval=}'
