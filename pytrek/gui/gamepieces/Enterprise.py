
from logging import Logger
from logging import getLogger

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import RadianInfo
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion

from pytrek.LocateResources import LocateResources


class Enterprise(
    GamePiece,
    SmoothMotion
):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='EnterpriseD.png')
        self.imageRotation = 0
        GamePiece.__init__(self, filename=fqFileName)
        SmoothMotion.__init__(self, imageRotation=125)

    def update(self):

        if self.inMotion is True:

            radianInfo: RadianInfo = self.computeArcadeMotion(currentPoint=ArcadePoint(x=self.center_x, y=self.center_y),
                                                              destinationPoint=self.destinationPoint,
                                                              spriteRotationAngle=self.angle,
                                                              rotationalSpeed=self.rotationSpeed)

            self.doMotion(gamePiece=self, destinationPoint=self.destinationPoint,
                          angleDiffRadians=radianInfo.angleDiffRadians, actualAngleRadians=radianInfo.actualAngleRadians)
