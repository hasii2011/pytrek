
from typing import List

from arcade import Sound
from arcade import Sprite
from arcade import Texture


class EnterpriseTorpedoExplosion(Sprite):

    DELAY_FRAMES: int = 8

    def __init__(self, textureList: List[Texture], sound: Sound):

        super().__init__()

        self._textures:     List[Texture] = textureList
        self._sound:        Sound         = sound
        self._textureIdx:   int           = 0
        self._delayCounter: int           = 0

        self.texture = self._textures[0]

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self._delayCounter += 1
        if self._delayCounter > EnterpriseTorpedoExplosion.DELAY_FRAMES:
            self._textureIdx += 1
            if self._textureIdx < len(self._textures):
                self.texture = self._textures[self._textureIdx]
            else:
                self.remove_from_sprite_lists()
            self._delayCounter = 0
