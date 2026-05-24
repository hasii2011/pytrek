from logging import Logger
from logging import getLogger
from typing import cast

from src.pytrek.engine.ArcadePoint import ArcadePoint
from src.pytrek.gui.gamepieces.base.BaseEnemy import EnemyId

from src.pytrek.gui.gamepieces.GamePiece import GamePiece
from src.pytrek.gui.gamepieces.GamePieceTypes import PhotonTorpedoId
from src.pytrek.gui.gamepieces.SmoothMotion import SmoothMotion
from src.pytrek.gui.gamepieces.SmoothMotion import RadianInfo


class PhotonTorpedo(GamePiece, SmoothMotion):

    FILENAME: str = 'PhotonTorpedo.png'
    nextId: int = 0

    def __init__(self, speed: float = 3.0):

        GamePiece.__init__(self, filename=PhotonTorpedo.FILENAME, speed=speed)
        SmoothMotion.__init__(self, imageRotation=0)

        self.logger: Logger = getLogger(__name__)

        self._id:      PhotonTorpedoId = PhotonTorpedoId(f'Torpedo-{PhotonTorpedo.nextId}')
        self._firedAt: EnemyId         = cast(EnemyId, None)

        PhotonTorpedo.nextId += 1

    @property
    def id(self) -> PhotonTorpedoId:
        return self._id

    @property
    def firedAt(self) -> EnemyId:
        return self._firedAt

    @firedAt.setter
    def firedAt(self, klingonId: EnemyId):
        self._firedAt = klingonId

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):

        if self.inMotion is True:

            radianInfo: RadianInfo = self.computeArcadeMotion(currentPoint=ArcadePoint(x=self.center_x, y=self.center_y),
                                                              destinationPoint=self.destinationPoint,
                                                              spriteRotationAngle=self.angle,
                                                              rotationalSpeed=self.rotationSpeed)

            self.doMotion(gamePiece=self, destinationPoint=self.destinationPoint,
                          angleDiffRadians=radianInfo.angleDiffRadians, actualAngleRadians=radianInfo.actualAngleRadians)
