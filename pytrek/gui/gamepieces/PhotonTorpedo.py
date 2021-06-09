from logging import Logger
from logging import getLogger
from typing import cast

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.Klingon import KlingonId

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import PhotonTorpedoId

from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion
from pytrek.gui.gamepieces.SmoothMotion import RadianInfo


class PhotonTorpedo(GamePiece, SmoothMotion):

    FILENAME: str = 'PhotonTorpedo.png'
    nextId: int = 0

    def __init__(self):

        GamePiece.__init__(self, filename=PhotonTorpedo.FILENAME)
        SmoothMotion.__init__(self, imageRotation=0)

        self.logger: Logger = getLogger(__name__)

        self._id:      PhotonTorpedoId = PhotonTorpedoId(f'Torpedo-{PhotonTorpedo.nextId}')
        self._firedAt: KlingonId       = cast(KlingonId, None)

        self.speed = 3  # TODO make this a game setting so we can tweak it for playability

        PhotonTorpedo.nextId += 1

    @property
    def id(self) -> PhotonTorpedoId:
        return self._id

    @property
    def firedAt(self) -> KlingonId:
        return self._firedAt

    @firedAt.setter
    def firedAt(self, klingonId: KlingonId):
        self._firedAt = klingonId

    def update(self):

        if self.inMotion is True:

            radianInfo: RadianInfo = self.computeArcadeMotion(currentPoint=ArcadePoint(x=self.center_x, y=self.center_y),
                                                              destinationPoint=self.destinationPoint,
                                                              spriteRotationAngle=self.angle,
                                                              rotationalSpeed=self.rotationSpeed)

            self.doMotion(gamePiece=self, destinationPoint=self.destinationPoint,
                          angleDiffRadians=radianInfo.angleDiffRadians, actualAngleRadians=radianInfo.actualAngleRadians)
