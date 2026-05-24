
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
import pyglet.media as media

from arcade import color
from arcade import Text

from arcade import SpriteSheet
from arcade import set_background_color

from arcade.particles import Emitter
from arcade.particles import make_interval_emitter

from src.pytrek.LocateResources import LocateResources

from src.pytrek.SoundMachine import SoundMachine
from src.pytrek.SoundMachine import SoundType

from src.pytrek.gui.UITypes import TextureList

from src.pytrek.gui.BaseSection import BaseSection

PARTICLE_SPEED_FAST:       float = 1.0
DEFAULT_EMIT_INTERVAL:     float = 0.003
DEFAULT_EMIT_DURATION:     float = 1.5
DEFAULT_SCALE:             float = 1.0
DEFAULT_PARTICLE_LIFETIME_MIN: float = 3.0
DEFAULT_PARTICLE_LIFETIME_MAX: float = 4.0

DEFAULT_ALPHA: int = 32


class WarpEffectSection(BaseSection):

    def __init__(self, width: int, height: int):
        self.logger: Logger = getLogger(__name__)

        super().__init__(left=0, bottom=0, width=width, height=height, modal=True, enabled=False)

        self._soundMachine:       SoundMachine        = SoundMachine()
        self._centerPosition:     Tuple[float, float] = (width / 2, height / 2)
        self._warpEffectTextures: TextureList         = self._loadWarpEffectTextures()

        self._warpingText: Text = Text(
            text='Warping: ',
            x=10,
            y=30,
            font_size=12,
            color=color.PALE_GOLD,
        )

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
        # start_render()

        self._emitter.draw()
        if self.isEffectComplete() is False:
            # draw_text("Warping: " + str(self._emitter.get_count()), 10, 30, color.PALE_GOLD, 12)
            self._warpingText.text = f'Warping: {self._emitter.get_count()}'
            self._warpingText.draw()
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

        # 3.3.3 way to create a continuous emitter
        e: Emitter = make_interval_emitter(
            center_xy=self._centerPosition,
            filenames_and_textures=[texture0, texture2],
            # filenames_and_textures=self._warpEffectTextures,
            emit_interval=DEFAULT_EMIT_INTERVAL,
            emit_duration=DEFAULT_EMIT_DURATION,
            particle_speed=PARTICLE_SPEED_FAST,
            particle_lifetime_min=DEFAULT_PARTICLE_LIFETIME_MIN,
            particle_lifetime_max=DEFAULT_PARTICLE_LIFETIME_MAX
        )

        return e

    def _loadWarpEffectTextures(self) -> TextureList:

        nColumns:     int = 4
        tileCount:    int = 4
        spriteWidth:  int = 32
        spriteHeight: int = 32
        bareFileName: str = f'WarpEffectSpriteSheet.png'
        fqFileName:   str = LocateResources.getImagePath(bareFileName=bareFileName)

        sheet: SpriteSheet = SpriteSheet(fqFileName)
        textures = sheet.get_texture_grid(
            size=(spriteWidth, spriteHeight),  # Replaces sprite_width and sprite_height
            columns=nColumns,  # Same as before
            count=tileCount  # Replaces tilecount
        )

        return TextureList(textures)
