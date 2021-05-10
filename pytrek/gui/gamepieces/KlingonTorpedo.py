
from uuid import uuid4

from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePosition import ArcadePosition

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion


class KlingonTorpedo(GamePiece, SmoothMotion):

    def __init__(self):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='KlingonTorpedo.png')

        GamePiece.__init__(self, filename=fqFileName)
        SmoothMotion.__init__(self)

        self._uuid: uuid4 = uuid4()

    @property
    def uuid(self) -> uuid4:
        return self._uuid

    def update(self):

        if self.inMotion is True:
            actualAngleRadians, angleDiffRadians = self.computeArcadeMotion(currentPoint=ArcadePosition(x=self.center_x, y=self.center_y),
                                                                            destinationPoint=self.destinationPoint,
                                                                            spriteRotationAngle=self.angle,
                                                                            rotationalSpeed=self.rotationSpeed)
            self.doMotion(gamePiece=self, destinationPoint=self.destinationPoint, angleDiffRadians=angleDiffRadians, actualAngleRadians=actualAngleRadians)
