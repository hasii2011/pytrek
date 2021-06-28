
from typing import List

from arcade import Sound
from arcade import Sprite
from arcade import Texture


class Explosion(Sprite):

    DELAY_FRAMES: int = 8

    def __init__(self, textureList: List[Texture], sound: Sound):

        super().__init__()

        self._textures: List[Texture] = textureList
        self._sound:    Sound         = sound

        self.textureIdx:    int     = 0
        self.texture:       Texture = self._textures[0]
        self._delayCounter: int     = 0

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self._delayCounter += 1
        if self._delayCounter > Explosion.DELAY_FRAMES:
            self.textureIdx += 1
            if self.textureIdx < len(self._textures):
                self.texture = self._textures[self.textureIdx]
            else:
                self.remove_from_sprite_lists()
            self._delayCounter = 0
