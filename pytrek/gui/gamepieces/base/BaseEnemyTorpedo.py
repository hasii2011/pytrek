from logging import Logger
from logging import getLogger
from typing import cast

from arcade import SpriteList

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer

from pytrek.gui.gamepieces.base.BaseEnemy import EnemyId
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import EnemyTorpedoId
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion
from pytrek.gui.gamepieces.SmoothMotion import RadianInfo

from pytrek.model.Coordinates import Coordinates


class BaseEnemyTorpedo(GamePiece, SmoothMotion):

    def __init__(self, filename: str, torpedoId: EnemyTorpedoId, speed: float = 3, scale: float = 1.0):

        GamePiece.__init__(self, filename=filename, speed=speed, scale=scale)
        SmoothMotion.__init__(self)

        self._baseEnemyTorpedoLogger: Logger = getLogger(__name__)

        self._id: EnemyTorpedoId = torpedoId

        self._firedBy:           EnemyId     = cast(EnemyId, None)
        self._firedFromPosition: Coordinates = cast(Coordinates, None)
        self._followers:         SpriteList  = cast(SpriteList, None)

        self._computer: Computer = Computer()

    @property
    def id(self) -> EnemyTorpedoId:
        return self._id

    @property
    def firedBy(self) -> EnemyId:
        """
        Returns: The ID of the Klingon who fire the torpedo
        """
        return self._firedBy

    @firedBy.setter
    def firedBy(self, klingonId: EnemyId):
        self._firedBy = klingonId

    @property
    def firedFromPosition(self) -> Coordinates:
        return self._firedFromPosition

    @firedFromPosition.setter
    def firedFromPosition(self, newValue: Coordinates):
        self._firedFromPosition = newValue
        self.currentPosition    = newValue

    @property
    def followers(self) -> SpriteList:
        return self._followers

    @followers.setter
    def followers(self, newValues: SpriteList):
        """
        Reference back to global follower list

        Args:
            newValues:
        """
        self._followers = newValues

    def update(self):

        if self.inMotion is True:
            radianInfo: RadianInfo = self.computeArcadeMotion(currentPoint=ArcadePoint(x=self.center_x, y=self.center_y),
                                                              destinationPoint=self.destinationPoint,
                                                              spriteRotationAngle=self.angle,
                                                              rotationalSpeed=self.rotationSpeed)

            # self._baseEnemyTorpedoLogger.debug(f'{radianInfo=} {self.destinationPoint=}')
            self.doMotion(gamePiece=self, destinationPoint=self.destinationPoint,
                          angleDiffRadians=radianInfo.angleDiffRadians, actualAngleRadians=radianInfo.actualAngleRadians)
            # self.doMotion2(gamePiece=self, destinationPoint=self.destinationPoint)

            self._potentiallyCreateAFollower()

    def _potentiallyCreateAFollower(self):
        """
        Only create one if we have entered another sector
        """
        currentX: float = self.center_x
        currentY: float = self.center_y
        position: Coordinates = self._computer.computeSectorCoordinates(x=currentX, y=currentY)

        if position != self.currentPosition:
            self._baseEnemyTorpedoLogger.debug(f'Created a follower @ {position}')
            self._placeTorpedoFollower(x=currentX, y=currentY)
            self.currentPosition = position

    def _placeTorpedoFollower(self, x: float, y: float):
        """
        Must be implemented by subclass to create correct follower

        Args:
            x:  Arcade x
            y:  Arcade y
        """
        pass
