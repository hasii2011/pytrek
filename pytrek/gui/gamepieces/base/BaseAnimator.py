
from typing import List
from typing import NewType

from arcade import Sprite
from arcade import Texture

TextureList = NewType('TextureList', List[Texture])


class BaseAnimator(Sprite):

    def __init__(self, textureList: TextureList, delayFrames: int, scale: float = 1.0):

        super().__init__(scale=scale)

        self._textures:    TextureList = textureList

        self._delayFrames:  int = delayFrames
        self._textureIdx:   int = 0
        self._delayCounter: int = 0

        # Prime the pump
        self.texture          = self._textures[0]

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self._delayCounter += 1
        if self._delayCounter > self._delayFrames:
            self._textureIdx += 1
            if self._textureIdx < len(self._textures):
                self.texture = self._textures[self._textureIdx]
            else:
                self.remove_from_sprite_lists()
            self._delayCounter = 0
