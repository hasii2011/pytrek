
from typing import cast

from logging import Logger
from logging import getLogger

from random import choice as randomChoice

# noinspection PyPackageRequirements
import pyglet.media as media

from arcade import Emitter
from arcade import EmitterIntervalWithTime
from arcade import LifetimeParticle
from arcade import Sound
from arcade import View
from arcade import color
from arcade import draw_text
from arcade import load_spritesheet
from arcade import rand_on_circle
from arcade import set_background_color
from arcade import start_render

from arcade import key as arcadeKey

from pytrek.LocateResources import LocateResources
from pytrek.gui.gamepieces.base.BaseAnimator import TextureList
from pytrek.mediators.base.BaseMediator import BaseMediator

PARTICLE_SPEED_FAST:       float = 1.0
DEFAULT_EMIT_INTERVAL:     float = 0.003
DEFAULT_EMIT_DURATION:     float = 1.5
DEFAULT_SCALE:             float = 1.0
DEFAULT_PARTICLE_LIFETIME: float = 3.0

DEFAULT_ALPHA: int = 32


class WarpEffect(View):
    """
    """
    def __init__(self, screenWidth: int, screenHeight: int):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._centerPosition: tuple[float, float] = (screenWidth / 2, screenHeight / 2)

        self._warpEffectTextures: TextureList = self._loadWarpEffectTextures()
        # If you have sprite lists, you should create them here,
        # and set them to None
        self._emitter: Emitter      = cast(Emitter, None)
        self._media:   media.Player = cast(media.Player, None)

        self._soundWarp: Sound = BaseMediator.loadSound('warp.wav')
        self._playing: bool = False

        set_background_color(color.BLACK)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self._emitter = self._createWarpEffectEmitter()
        self._playing = False

    def isEffectComplete(self) -> bool:
        return self._emitter.can_reap()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        start_render()
        self._emitter.draw()
        draw_text("Warping: " + str(self._emitter.get_count()), 10, 30, color.PALE_GOLD, 12)

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time: float):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self._emitter.update()
        if self._playing is False:
            self._media = self._soundWarp.play(volume=1.0)
            self._playing = True

    def on_key_release(self, releasedKey: int, key_modifiers: int):

        if releasedKey == arcadeKey.A:
            self.setup()
        if releasedKey == arcadeKey.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def _createWarpEffectEmitter(self) -> Emitter:
        """
        Random particle textures
        """
        texture0 = self._warpEffectTextures[0]
        texture2 = self._warpEffectTextures[2]

        e: Emitter = Emitter(
            center_xy=self._centerPosition,
            emit_controller=EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
            particle_factory=lambda emitter: LifetimeParticle(
                filename_or_texture=randomChoice((texture0, texture2)),
                change_xy=rand_on_circle((0.0, 0.0), PARTICLE_SPEED_FAST),
                lifetime=DEFAULT_PARTICLE_LIFETIME,
                scale=DEFAULT_SCALE
            )
        )

        return e

    def _loadWarpEffectTextures(self) -> TextureList:

        nColumns:  int = 4
        tileCount: int = 4
        spriteWidth:  int = 32
        spriteHeight: int = 32
        bareFileName: str = f'WarpEffectSpriteSheet.png'
        fqFileName:   str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

        textureList: TextureList = cast(TextureList, load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount))

        return textureList
