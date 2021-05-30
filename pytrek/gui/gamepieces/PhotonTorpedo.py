from logging import Logger
from logging import getLogger
from typing import cast

from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import KlingonId
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion


class PhotonTorpedo(GamePiece, SmoothMotion):

    nextId: int = 0

    def __init__(self):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='PhotonTorpedo.png')

        GamePiece.__init__(self, filename=fqFileName)
        SmoothMotion.__init__(self, imageRotation=0)

        self.logger: Logger = getLogger(__name__)

        self._id:      int       = PhotonTorpedo.nextId
        self._firedAt: KlingonId = cast(KlingonId, None)

        PhotonTorpedo.nextId += 1

    @property
    def firedAt(self) -> KlingonId:
        return self._firedAt

    @firedAt.setter
    def firedAt(self, klingonId: KlingonId):
        self._firedAt = klingonId

    def update(self):

        if self.inMotion is True:

            actualAngleRadians, angleDiffRadians = self.computeArcadeMotion(currentPoint=ArcadePoint(x=self.center_x, y=self.center_y),
                                                                            destinationPoint=self.destinationPoint,
                                                                            spriteRotationAngle=self.angle,
                                                                            rotationalSpeed=self.rotationSpeed)
            self.doMotion(gamePiece=self, destinationPoint=self.destinationPoint, angleDiffRadians=angleDiffRadians, actualAngleRadians=actualAngleRadians)
