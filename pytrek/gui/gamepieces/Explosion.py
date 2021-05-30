
from typing import List

from arcade import Sound
from arcade import Sprite
from arcade import Texture


class Explosion(Sprite):

    DELAY_FRAMES: int =8

    def __init__(self, textureList: List[Texture], sound: Sound):

        super().__init__()

        self.textures: List[Texture] = textureList
        self.sound:    Sound         = sound

        self.textureIdx:    int     = 0
        self.texture:       Texture = self.textures[0]
        self._delayCounter: int     = 0

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self._delayCounter += 1
        if self._delayCounter > Explosion.DELAY_FRAMES:
            self.textureIdx += 1
            print(f"Change texture")
            if self.textureIdx < len(self.textures):
                self.texture = self.textures[self.textureIdx]
                # self.sound.play()
            else:
                self.remove_from_sprite_lists()
            self._delayCounter = 0
