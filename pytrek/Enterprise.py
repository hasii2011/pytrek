
from typing import List

from logging import Logger
from logging import getLogger

from arcade import Sprite
from arcade import load_texture
from arcade import Texture

from pytrek.LocateResources import LocateResources

SPRITE_SCALING: float = 1.0

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT:  int = 0
TEXTURE_RIGHT: int = 1


class Enterprise(Sprite):

    def __init__(self):

        super().__init__()

        self.scale:    float         = SPRITE_SCALING
        self.textures: List[Texture] = []

        self.logger: Logger = getLogger(__name__)
        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           resourcesPath=LocateResources.IMAGE_RESOURCES_PATH,
                                                           bareFileName='EnterpriseD.png')
        texture = load_texture(fqFileName)
        self.textures.append(texture)
        texture = load_texture(fqFileName, flipped_horizontally=True)
        self.textures.append(texture)

        # By default, face right.
        self.texture = texture

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
            self.logger.debug(f'TEXTURE_LEFT')
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]
            self.logger.debug(f'TEXTURE_RIGHT')
