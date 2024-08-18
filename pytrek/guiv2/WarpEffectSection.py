
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from random import choice as randomChoice

# noinspection PyPackageRequirements
import pyglet.media as media

from arcade import Emitter
from arcade import EmitterIntervalWithTime
from arcade import LifetimeParticle

from arcade import color
from arcade import draw_text
from arcade import load_spritesheet
from arcade import rand_on_circle
from arcade import set_background_color
from arcade import start_render

from pytrek.LocateResources import LocateResources

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType

from pytrek.gui.UITypes import TextureList

from pytrek.guiv2.BaseSection import BaseSection

PARTICLE_SPEED_FAST:       float = 1.0
DEFAULT_EMIT_INTERVAL:     float = 0.003
DEFAULT_EMIT_DURATION:     float = 1.5
DEFAULT_SCALE:             float = 1.0
DEFAULT_PARTICLE_LIFETIME: float = 3.0

DEFAULT_ALPHA: int = 32


class WarpEffectSection(BaseSection):

    def __init__(self, width: int, height: int):
        self.logger: Logger = getLogger(__name__)

        super().__init__(left=0, bottom=0, width=width, height=height, modal=True, enabled=False)

        self._soundMachine:       SoundMachine        = SoundMachine()
        self._centerPosition:     Tuple[float, float] = (width / 2, height / 2)
        self._warpEffectTextures: TextureList         = self._loadWarpEffectTextures()

        self._emitter: Emitter      = cast(Emitter, None)
        self._media:   media.Player = cast(media.Player, None)

        self._playing: bool = False

        set_background_color(color.BLACK)

    def setup(self):
        """
        Call this to restart the emitter
        """
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
        if self.isEffectComplete() is False:
            draw_text("Warping: " + str(self._emitter.get_count()), 10, 30, color.PALE_GOLD, 12)
        self.drawDebug()

    def on_update(self, delta_time: float):
        """
        """
        self._emitter.update()
        if self._playing is False:
            self._media = self._soundMachine.playSound(SoundType.Warp)
            self._playing = True

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

        nColumns:     int = 4
        tileCount:    int = 4
        spriteWidth:  int = 32
        spriteHeight: int = 32
        bareFileName: str = f'WarpEffectSpriteSheet.png'
        fqFileName:   str = LocateResources.getImagePath(bareFileName=bareFileName)

        textureList: TextureList = cast(TextureList, load_spritesheet(fqFileName, spriteWidth, spriteHeight, nColumns, tileCount))

        return textureList
