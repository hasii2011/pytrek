"""
Used to test sprites that used a time based tiled image sheet to display themselves
"""
from typing import cast

from arcade import SpriteList
from arcade import Window
from arcade import color
from arcade import draw_text

from arcade import set_background_color
from arcade import start_render

from arcade import run as arcadeRun
from arcade import key as arcadeKey

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList

from pytrek.gui.gamepieces.PhaserBolt import PhaserBolt
from pytrek.gui.gamepieces.PhotonTorpedoExplosion import PhotonTorpedoExplosion

from pytrek.gui.gamepieces.commander.CommanderTorpedoExplosion import CommanderTorpedoExplosion
from pytrek.gui.gamepieces.klingon.KlingonTorpedoExplosion import KlingonTorpedoExplosion
from pytrek.gui.gamepieces.supercommander.SuperCommanderTorpedoExplosion import SuperCommanderTorpedoExplosion

from pytrek.mediators.CommanderTorpedoMediator import CommanderTorpedoMediator
from pytrek.mediators.EnterprisePhaserMediator import EnterprisePhaserMediator
from pytrek.mediators.EnterpriseTorpedoMediator import EnterpriseTorpedoMediator
from pytrek.mediators.KlingonTorpedoMediator import KlingonTorpedoMediator
from pytrek.mediators.SuperCommanderTorpedoMediator import SuperCommanderTorpedoMediator

from pytrek.LocateResources import LocateResources

from pytrek.settings.SettingsCommon import SettingsCommon

SCREEN_WIDTH:  int = 800
SCREEN_HEIGHT: int = 600

HALF_SCREEN_WIDTH:  int = SCREEN_WIDTH // 2
HALF_SCREEN_HEIGHT: int = SCREEN_HEIGHT // 2

TITLE_X: int = HALF_SCREEN_WIDTH - 32
TITLE_Y: int = SCREEN_HEIGHT - 32

TITLE_TORPEDO_X_OFFSET: int = 80
TITLE_TORPEDO_Y_OFFSET: int = 48

EXPLOSION_X_OFFSET: int = 200
EXPLOSION_Y_OFFSET: int = 200


SCREEN_TITLE:    str = "Test Sprite Sheet"
EXPLOSION_TITLE: str = 'Explosions'


class TestExplosions(Window):
    """
    """
    ETX_COLOR = color.WHITE

    def __init__(self, width: int, height: int, title: str):

        super().__init__(width, height, title)

        set_background_color(color.BLACK)

        self._sprites:     SpriteList = SpriteList()

        em:  EnterpriseTorpedoMediator     = EnterpriseTorpedoMediator()
        km:  KlingonTorpedoMediator        = KlingonTorpedoMediator()
        cm:  CommanderTorpedoMediator      = CommanderTorpedoMediator()
        sm:  SuperCommanderTorpedoMediator = SuperCommanderTorpedoMediator()
        epm: EnterprisePhaserMediator      = EnterprisePhaserMediator()

        self._enterpriseTorpedoExplosionTextures:     TextureList = em.torpedoExplosionTextures
        self._klingonTorpedoExplosionTextures:        TextureList = km.torpedoExplosionTextures
        self._commanderTorpedoExplosionTextures:      TextureList = cm.torpedoExplosionTextures
        self._superCommanderTorpedoExplosionTextures: TextureList = sm.torpedoExplosionTextures
        self._phaserFireTextures:                     TextureList = epm.phaserFireTextures()

        self._etxPoint:        ArcadePoint = cast(ArcadePoint, None)
        self._ktxPoint:        ArcadePoint = cast(ArcadePoint, None)
        self._ctxPoint:        ArcadePoint = cast(ArcadePoint, None)
        self._stxPoint:        ArcadePoint = cast(ArcadePoint, None)
        self._phaserFirePoint: ArcadePoint = cast(ArcadePoint, None)

    def setup(self):
        """
        Set up the game here. Call this function to restart the game.
        """

        enterpriseTorpedoExplosion:     PhotonTorpedoExplosion     = self._getEnterpriseTorpedoExplosion()
        klingonTorpedoExplosion:        KlingonTorpedoExplosion        = self._getKlingonTorpedoExplosion()
        commanderTorpedoExplosion:      CommanderTorpedoExplosion      = self._getCommanderTorpedoExplosion()
        superCommanderTorpedoExplosion: SuperCommanderTorpedoExplosion = self._getSuperCommanderTorpedoExplosion()
        phaserFire:                     PhaserBolt                     = self._getPhaserFire()

        self._sprites.append(enterpriseTorpedoExplosion)
        self._sprites.append(klingonTorpedoExplosion)
        self._sprites.append(commanderTorpedoExplosion)
        self._sprites.append(superCommanderTorpedoExplosion)
        self._sprites.append(phaserFire)

    @property
    def enterpriseTorpedoExplosionPoint(self) -> ArcadePoint:

        if self._etxPoint is None:
            self._etxPoint = ArcadePoint(x=HALF_SCREEN_WIDTH // 2, y=HALF_SCREEN_HEIGHT // 2)

        return self._etxPoint

    @property
    def klingonTorpedoExplosionPoint(self) -> ArcadePoint:
        if self._ktxPoint is None:
            self._ktxPoint = ArcadePoint(x=HALF_SCREEN_WIDTH + EXPLOSION_X_OFFSET, y=HALF_SCREEN_HEIGHT + EXPLOSION_Y_OFFSET)

        return self._ktxPoint

    @property
    def commanderTorpedoExplosionPoint(self) -> ArcadePoint:
        if self._ctxPoint is None:
            self._ctxPoint = ArcadePoint(x=HALF_SCREEN_WIDTH - EXPLOSION_X_OFFSET, y=HALF_SCREEN_HEIGHT + EXPLOSION_Y_OFFSET)

        return self._ctxPoint

    @property
    def superCommanderTorpedoExplosionPoint(self) -> ArcadePoint:
        if self._stxPoint is None:
            self._stxPoint = ArcadePoint(x=HALF_SCREEN_WIDTH + EXPLOSION_X_OFFSET, y=HALF_SCREEN_HEIGHT - EXPLOSION_Y_OFFSET)

        return self._stxPoint

    @property
    def phaserFirePoint(self) -> ArcadePoint:

        if self._phaserFirePoint is None:
            x: int = HALF_SCREEN_WIDTH + (HALF_SCREEN_WIDTH // 2)
            self._phaserFirePoint = ArcadePoint(x=x, y=HALF_SCREEN_HEIGHT)

        return self._phaserFirePoint

    def on_draw(self):
        """
        Render the screen./////
        """
        start_render()
        draw_text(EXPLOSION_TITLE, TITLE_X, TITLE_Y, color=TestExplosions.ETX_COLOR, font_size=16)

        self._sprites.draw()
        self._drawEnterpriseTorpedoExplosionTitle()
        self._drawKlingonTorpedoExplosionTitle()
        self._drawCommanderTorpedoExplosionTitle()
        self._drawSuperCommanderTorpedoExplosionTitle()
        self._drawPhaserFireTitle()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self._sprites.update()

    def on_key_release(self, releasedKey: int, key_modifiers: int):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if releasedKey == arcadeKey.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)
        elif releasedKey == arcadeKey.A:
            self.setup()

    def _getEnterpriseTorpedoExplosion(self) -> PhotonTorpedoExplosion:

        explosion: PhotonTorpedoExplosion = PhotonTorpedoExplosion(textureList=self._enterpriseTorpedoExplosionTextures)

        etxPoint: ArcadePoint = self.enterpriseTorpedoExplosionPoint
        explosion.center_x = etxPoint.x
        explosion.center_y = etxPoint.y

        return explosion

    def _getKlingonTorpedoExplosion(self) -> KlingonTorpedoExplosion:

        explosion: KlingonTorpedoExplosion = KlingonTorpedoExplosion(textureList=self._klingonTorpedoExplosionTextures)

        ktxPoint: ArcadePoint = self.klingonTorpedoExplosionPoint

        explosion.center_x = ktxPoint.x
        explosion.center_y = ktxPoint.y

        return explosion

    def _getCommanderTorpedoExplosion(self) -> CommanderTorpedoExplosion:

        explosion: CommanderTorpedoExplosion = CommanderTorpedoExplosion(textureList=self._commanderTorpedoExplosionTextures)

        ctxPoint: ArcadePoint = self.commanderTorpedoExplosionPoint

        explosion.center_x = ctxPoint.x
        explosion.center_y = ctxPoint.y

        return explosion

    def _getSuperCommanderTorpedoExplosion(self) -> SuperCommanderTorpedoExplosion:

        explosion: SuperCommanderTorpedoExplosion = SuperCommanderTorpedoExplosion(textureList=self._superCommanderTorpedoExplosionTextures)

        stxPoint: ArcadePoint = self.superCommanderTorpedoExplosionPoint
        explosion.center_x = stxPoint.x
        explosion.center_y = stxPoint.y

        return explosion

    def _getPhaserFire(self) -> PhaserBolt:

        phaserFire: PhaserBolt = PhaserBolt(textureList=self._phaserFireTextures)

        arcadePoint: ArcadePoint = self.phaserFirePoint

        phaserFire.center_x = arcadePoint.x
        phaserFire.center_y = arcadePoint.y

        return phaserFire

    def _drawEnterpriseTorpedoExplosionTitle(self):

        etxPoint: ArcadePoint = self.enterpriseTorpedoExplosionPoint
        msg:      str         = 'Enterprise Torpedo'
        # draw_text(msg, etxPoint.x, etxPoint.y, color=MessageConsole.CONSOLE_TEXT_COLOR,
        #           font_size=MessageConsole.CONSOLE_FONT_SIZE, font_name=FIXED_WIDTH_FONT_NAME)
        draw_text(msg, etxPoint.x - TITLE_TORPEDO_X_OFFSET, etxPoint.y - TITLE_TORPEDO_Y_OFFSET, color=TestExplosions.ETX_COLOR)

    def _drawKlingonTorpedoExplosionTitle(self):

        ktxPoint: ArcadePoint = self.klingonTorpedoExplosionPoint
        msg:      str         = 'Klingon Torpedo'

        draw_text(msg, ktxPoint.x - TITLE_TORPEDO_X_OFFSET, ktxPoint.y - TITLE_TORPEDO_Y_OFFSET, color=TestExplosions.ETX_COLOR)

    def _drawCommanderTorpedoExplosionTitle(self):

        ctxPoint: ArcadePoint = self.commanderTorpedoExplosionPoint
        msg:      str         = 'Commander Torpedo'

        draw_text(msg, ctxPoint.x - TITLE_TORPEDO_X_OFFSET, ctxPoint.y - TITLE_TORPEDO_Y_OFFSET, color=TestExplosions.ETX_COLOR)

    def _drawSuperCommanderTorpedoExplosionTitle(self):

        stxPoint: ArcadePoint = self.superCommanderTorpedoExplosionPoint
        msg:      str         = 'Super Commander Torpedo'

        draw_text(msg, stxPoint.x - TITLE_TORPEDO_X_OFFSET, stxPoint.y - TITLE_TORPEDO_Y_OFFSET, color=TestExplosions.ETX_COLOR)

    def _drawPhaserFireTitle(self):

        pfPoint: ArcadePoint = self.phaserFirePoint
        msg: str = 'Phaser Fire Effect'
        draw_text(msg, pfPoint.x - 80, pfPoint.y - TITLE_TORPEDO_Y_OFFSET, color=TestExplosions.ETX_COLOR)


def main():
    """
    Main method
    """
    LocateResources.setupSystemLogging()
    SettingsCommon.determineSettingsLocation()

    window: TestExplosions = TestExplosions(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeRun()


if __name__ == "__main__":
    main()
