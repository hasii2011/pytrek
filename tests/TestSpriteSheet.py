"""
"""
from typing import List
from typing import cast

from arcade import Sound
from arcade import SpriteList
from arcade import Texture
from arcade import Window
from arcade import color

from arcade import set_background_color
from arcade import start_render
from arcade import load_spritesheet

from arcade import run as arcadeRun
from arcade import key as arcadeKey

from pytrek.LocateResources import LocateResources

from pytrek.gui.gamepieces.EnterpriseTorpedoExplosion import EnterpriseTorpedoExplosion

SCREEN_WIDTH:  int = 800
SCREEN_HEIGHT: int = 600
SCREEN_TITLE:  str = "Test Sprite Sheet"


class TestSpriteSheet(Window):
    """
    Main application class.
    """

    def __init__(self, width: int, height: int, title: str):

        super().__init__(width, height, title)

        set_background_color(color.BLACK)

        self._explosions:     SpriteList = SpriteList()
        self._explosionSound: Sound      = cast(Sound, None)

        self._torpedoTextures: List[Texture] = self._loadPhotonTorpedoExplosions()

    def setup(self):
        """
        Set up the game here. Call this function to restart the game.
        """
        explosion: EnterpriseTorpedoExplosion = EnterpriseTorpedoExplosion(textureList=self._torpedoTextures)
        explosion.center_x = SCREEN_WIDTH // 2
        explosion.center_y = SCREEN_HEIGHT // 2

        self._explosions.append(explosion)

        self._explosionSound = self._loadSound(bareFileName='SmallExplosion.wav')

    def on_draw(self):
        """
        Render the screen.
        """
        start_render()
        self._explosions.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self._explosions.update()

    def on_key_release(self, releasedKey: int, key_modifiers: int):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if releasedKey == arcadeKey.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)

    def _loadPhotonTorpedoExplosions(self) -> List[Texture]:
        """
        Cache the torpedo explosion textures

        Returns:  The texture list
        """
        nColumns:  int = 8
        tileCount: int = 21
        spriteWidth:  int = 128
        spriteHeight: int = 128
        bareFileName: str = f'EnterpriseTorpedoExplosionSheet.png'
        fqFileName:   str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

        explosions: List[Texture] = load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount)

        return explosions

    def _loadSound(self, bareFileName: str) -> Sound:

        fqFileName: str   = LocateResources.getResourcesPath(LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName)
        sound:      Sound = Sound(fqFileName)

        return sound


def main():
    """
    Main method
    """
    window: TestSpriteSheet = TestSpriteSheet(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeRun()


if __name__ == "__main__":
    main()
