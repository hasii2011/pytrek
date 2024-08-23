"""
Used to test sprites that used a time based tiled image sheet to display themselves
"""
from typing import cast

from arcade import SpriteList
from arcade import View
from arcade import Window
from arcade import color
from arcade import draw_line
from arcade import draw_text

from arcade import set_background_color
from arcade import start_render

from arcade import run as arcadeRun
from arcade import key as arcadeKey
from arcade.color import WHITE

from pytrek.Constants import COMMAND_SECTION_HEIGHT
from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList
from pytrek.gui.gamepieces.PhaserBolt import PhaserBolt
from pytrek.gui.gamepieces.PhotonTorpedoExplosion import PhotonTorpedoExplosion

from pytrek.gui.gamepieces.commander.CommanderTorpedoExplosion import CommanderTorpedoExplosion
from pytrek.gui.gamepieces.klingon.KlingonTorpedoExplosion import KlingonTorpedoExplosion
from pytrek.gui.gamepieces.supercommander.SuperCommanderTorpedoExplosion import SuperCommanderTorpedoExplosion
from pytrek.guiv2.MessageConsoleProxy import MessageConsoleProxy
from pytrek.gui.MessageConsoleSection import MessageConsoleSection

from pytrek.mediators.CommanderTorpedoMediator import CommanderTorpedoMediator
from pytrek.mediators.EnterprisePhaserMediator import EnterprisePhaserMediator
from pytrek.mediators.EnterpriseTorpedoMediator import EnterpriseTorpedoMediator
from pytrek.mediators.KlingonTorpedoMediator import KlingonTorpedoMediator
from pytrek.mediators.SuperCommanderTorpedoMediator import SuperCommanderTorpedoMediator

from tests.ProjectTestBase import ProjectTestBase

SCREEN_TITLE:    str = "Test Sprite Sheet"
EXPLOSION_TITLE: str = 'Explosions'
#
# New Constants
#
TITLE_X: int = SCREEN_WIDTH // 2 - 32
TITLE_Y: int = SCREEN_HEIGHT - 32

LINE_Y:       int = TITLE_Y - 10
LINE_START_X: int = 32
LINE_END_X:  int = SCREEN_WIDTH - 32

LEFT_X:   int = 125
OFFSET_Y: int = TITLE_Y - 96
INC_Y:    int = 150

TITLE_TORPEDO_X_OFFSET: int = 80
TITLE_TORPEDO_Y_OFFSET: int = 48

HELP_LINE_Y_OFFSET: int = 150
HELP_TEXT_X_OFFSET: int = 50
HELP_TEXT_Y_OFFSET: int = 32

HELP_TEXT_COLOR = WHITE


class AppTestExplosions(View):
    """
    """
    ETX_COLOR = color.WHITE

    def __init__(self):

        super().__init__()

        set_background_color(color.BLACK)

        self._messageConsole:   MessageConsoleSection = MessageConsoleSection(left=0,
                                                                              bottom=COMMAND_SECTION_HEIGHT,
                                                                              height=CONSOLE_SECTION_HEIGHT,
                                                                              width=SCREEN_WIDTH,
                                                                              accept_keyboard_events=False
                                                                              )
        self._messageConsoleProxy: MessageConsoleProxy = MessageConsoleProxy()
        self._messageConsoleProxy.console = self._messageConsole

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

        enterpriseTorpedoExplosion:     PhotonTorpedoExplosion         = self._getEnterpriseTorpedoExplosion()
        klingonTorpedoExplosion:        KlingonTorpedoExplosion        = self._getKlingonTorpedoExplosion()
        commanderTorpedoExplosion:      CommanderTorpedoExplosion      = self._getCommanderTorpedoExplosion()
        superCommanderTorpedoExplosion: SuperCommanderTorpedoExplosion = self._getSuperCommanderTorpedoExplosion()
        phaserFire:                     PhaserBolt                     = self._getPhaserFire()

        self._sprites.append(enterpriseTorpedoExplosion)
        self._sprites.append(klingonTorpedoExplosion)
        self._sprites.append(commanderTorpedoExplosion)
        self._sprites.append(superCommanderTorpedoExplosion)
        self._sprites.append(phaserFire)

        self.section_manager.add_section(self._messageConsole)

    @property
    def klingonTorpedoExplosionPoint(self) -> ArcadePoint:
        if self._ktxPoint is None:
            self._ktxPoint = ArcadePoint(x=LEFT_X, y=OFFSET_Y)

        return self._ktxPoint

    @property
    def commanderTorpedoExplosionPoint(self) -> ArcadePoint:
        if self._ctxPoint is None:
            x: float = self.klingonTorpedoExplosionPoint.x + LEFT_X * 2
            self._ctxPoint = ArcadePoint(x=x, y=OFFSET_Y)

        return self._ctxPoint

    @property
    def superCommanderTorpedoExplosionPoint(self) -> ArcadePoint:
        if self._stxPoint is None:
            x: float = self.commanderTorpedoExplosionPoint.x + LEFT_X * 2
            self._stxPoint = ArcadePoint(x=x, y=OFFSET_Y)

        return self._stxPoint

    @property
    def enterpriseTorpedoExplosionPoint(self) -> ArcadePoint:

        if self._etxPoint is None:
            y: float = self.klingonTorpedoExplosionPoint.y - INC_Y
            self._etxPoint = ArcadePoint(x=LEFT_X, y=y)

        return self._etxPoint

    @property
    def phaserFirePoint(self) -> ArcadePoint:

        if self._phaserFirePoint is None:
            x: float = self.superCommanderTorpedoExplosionPoint.x
            y: float = self.superCommanderTorpedoExplosionPoint.y - INC_Y
            self._phaserFirePoint = ArcadePoint(x=x, y=y)

        return self._phaserFirePoint

    def on_draw(self):
        """
        Render the screen.
        """
        start_render()
        draw_text(EXPLOSION_TITLE, TITLE_X, TITLE_Y, color=AppTestExplosions.ETX_COLOR, font_size=16)

        draw_line(start_x=LINE_START_X, start_y=LINE_Y, end_x=LINE_END_X, end_y=LINE_Y, color=WHITE, line_width=2)

        self._drawPhaserFireTitle()
        self._sprites.draw()
        self._drawEnterpriseTorpedoExplosionTitle()
        self._drawKlingonTorpedoExplosionTitle()
        self._drawCommanderTorpedoExplosionTitle()
        self._drawSuperCommanderTorpedoExplosionTitle()

        self._drawHelpText()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self._sprites.update()

    def on_key_release(self, releasedKey: int, key_modifiers: int):
        """
        Called whenever the user releases a previously pressed key.
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

        draw_text(msg, etxPoint.x - TITLE_TORPEDO_X_OFFSET, etxPoint.y - TITLE_TORPEDO_Y_OFFSET, color=AppTestExplosions.ETX_COLOR)

    def _drawKlingonTorpedoExplosionTitle(self):

        ktxPoint: ArcadePoint = self.klingonTorpedoExplosionPoint
        msg:      str         = 'Klingon Torpedo'

        draw_text(msg, ktxPoint.x - TITLE_TORPEDO_X_OFFSET, ktxPoint.y - TITLE_TORPEDO_Y_OFFSET, color=AppTestExplosions.ETX_COLOR)

    def _drawCommanderTorpedoExplosionTitle(self):

        ctxPoint: ArcadePoint = self.commanderTorpedoExplosionPoint
        msg:      str         = 'Commander Torpedo'

        draw_text(msg, ctxPoint.x - TITLE_TORPEDO_X_OFFSET, ctxPoint.y - TITLE_TORPEDO_Y_OFFSET, color=AppTestExplosions.ETX_COLOR)

    def _drawSuperCommanderTorpedoExplosionTitle(self):

        stxPoint: ArcadePoint = self.superCommanderTorpedoExplosionPoint
        msg:      str         = 'Super Commander Torpedo'

        draw_text(msg, stxPoint.x - TITLE_TORPEDO_X_OFFSET, stxPoint.y - TITLE_TORPEDO_Y_OFFSET, color=AppTestExplosions.ETX_COLOR)

    def _drawPhaserFireTitle(self):

        pfPoint: ArcadePoint = self.phaserFirePoint
        msg: str = 'Phaser Fire Effect'
        draw_text(msg, pfPoint.x - 80, pfPoint.y - TITLE_TORPEDO_Y_OFFSET, color=AppTestExplosions.ETX_COLOR)

    def _drawHelpText(self):

        y: float = self.enterpriseTorpedoExplosionPoint.y - HELP_LINE_Y_OFFSET

        draw_line(start_x=LINE_START_X, start_y=y, end_x=LINE_END_X, end_y=y, color=WHITE, line_width=2)

        y = y - HELP_TEXT_Y_OFFSET
        # noinspection SpellCheckingInspection
        draw_text("A - 'A'gain    Q - 'Q'uit", start_x=HELP_TEXT_X_OFFSET, start_y=y, color=HELP_TEXT_COLOR)


def main():
    """
    Main method
    """
    ProjectTestBase.setUpLogging()

    arcadeWindow: Window = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    arcadeWindow.background_color = color.BLACK
    arcadeWindow.clear()

    testView: AppTestExplosions = AppTestExplosions()
    testView.setup()
    arcadeWindow.show_view(testView)

    arcadeRun()


if __name__ == "__main__":
    main()
