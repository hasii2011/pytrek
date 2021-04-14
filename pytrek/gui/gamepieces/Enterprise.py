
from typing import List

from logging import Logger
from logging import getLogger

from arcade import load_texture
from arcade import Texture

from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion

from pytrek.LocateResources import LocateResources

SPRITE_SCALING: float = 1.0

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT:  int = 0
TEXTURE_RIGHT: int = 1


class Enterprise(GamePiece, SmoothMotion):

    def __init__(self):

        GamePiece.__init__(self)
        SmoothMotion.__init__(self)

        self.scale:    float         = SPRITE_SCALING
        self.textures: List[Texture] = []

        self.logger: Logger = getLogger(__name__)
        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='EnterpriseD.png')
        leftTexture = load_texture(fqFileName)
        self.textures.append(leftTexture)
        rightTexture = load_texture(fqFileName, flipped_horizontally=True)
        self.textures.append(rightTexture)

        # By default, face left.
        self.texture = leftTexture

        self._destination_point = None

    @property
    def destination_point(self):
        return self._destination_point

    @destination_point.setter
    def destination_point(self, destination_point):
        self._destination_point = destination_point

    def update(self):

        if self.inMotion is True:
            actualAngleRadians, angleDiffRadians = self.computeArcadeMotion(currentPoint=ArcadePosition(x=self.center_x, y=self.center_y),
                                                                            destinationPoint=self.destination_point,
                                                                            spriteRotationAngle=self.angle,
                                                                            rotationalSpeed=self.rotationSpeed)
            self.doMotion(gamePiece=self, destinationPoint=self.destination_point, angleDiffRadians=angleDiffRadians, actualAngleRadians=actualAngleRadians)
