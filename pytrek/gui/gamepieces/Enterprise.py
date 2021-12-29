
from logging import Logger
from logging import getLogger

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion
from pytrek.gui.gamepieces.SmoothMotion import RadianInfo


class Enterprise(
    GamePiece,
    SmoothMotion
):

    FILENAME: str = 'EnterpriseD.png'

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self.imageRotation = 0
        GamePiece.__init__(self, filename=Enterprise.FILENAME)
        SmoothMotion.__init__(self, imageRotation=125)

    def update(self):

        if self.inMotion is True:

            radianInfo: RadianInfo = self.computeArcadeMotion(currentPoint=ArcadePoint(x=self.center_x, y=self.center_y),
                                                              destinationPoint=self.destinationPoint,
                                                              spriteRotationAngle=self.angle,
                                                              rotationalSpeed=self.rotationSpeed)

            self.doMotion(gamePiece=self, destinationPoint=self.destinationPoint,
                          angleDiffRadians=radianInfo.angleDiffRadians, actualAngleRadians=radianInfo.actualAngleRadians)

    def __str__(self) -> str:

        depiction: str = (
            f'Enterprise('
            f'Sector coordinates={self.gameCoordinates}'
            f')'
        )
        return depiction

    def __repr__(self) -> str:
        return self.__str__()
