
from typing import List

from arcade import Texture

from pytrek.gui.gamepieces.GamePiece import GamePiece


class Explosion(
    GamePiece
):

    def __init__(self, textureList: List[Texture]):

        super().__init__()

        self._currentTexture: int = 0
        self._textures = textureList

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        if self._currentTexture < len(self._textures):
            self.set_texture(self._currentTexture)
        else:
            self.remove_from_sprite_lists()

        self._currentTexture += 1
