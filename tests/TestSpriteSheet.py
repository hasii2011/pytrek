"""
Used to test sprites that used a time based tiled image sheet to display themselves
"""

from arcade import SpriteList
from arcade import Window
from arcade import color

from arcade import set_background_color
from arcade import start_render

from arcade import run as arcadeRun
from arcade import key as arcadeKey

from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList

from pytrek.gui.gamepieces.EnterpriseTorpedoExplosion import EnterpriseTorpedoExplosion
from pytrek.gui.gamepieces.commander.CommanderTorpedoExplosion import CommanderTorpedoExplosion
from pytrek.gui.gamepieces.klingon.KlingonTorpedoExplosion import KlingonTorpedoExplosion
from pytrek.gui.gamepieces.supercommander.SuperCommanderTorpedoExplosion import SuperCommanderTorpedoExplosion
from pytrek.mediators.CommanderTorpedoMediator import CommanderTorpedoMediator

from pytrek.mediators.EnterpriseTorpedoMediator import EnterpriseTorpedoMediator
from pytrek.mediators.KlingonTorpedoMediator import KlingonTorpedoMediator

from pytrek.LocateResources import LocateResources
from pytrek.mediators.SuperCommanderTorpedoMediator import SuperCommanderTorpedoMediator

from pytrek.settings.SettingsCommon import SettingsCommon

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

        self._sprites:     SpriteList = SpriteList()

        em: EnterpriseTorpedoMediator     = EnterpriseTorpedoMediator()
        km: KlingonTorpedoMediator        = KlingonTorpedoMediator()
        cm: CommanderTorpedoMediator      = CommanderTorpedoMediator()
        sm: SuperCommanderTorpedoMediator = SuperCommanderTorpedoMediator()

        self._enterpriseTorpedoExplosionTextures:     TextureList = em.torpedoExplosionTextures
        self._klingonTorpedoExplosionTextures:        TextureList = km.torpedoExplosionTextures
        self._commanderTorpedoExplosionTextures:      TextureList = cm.torpedoExplosionTextures
        self._superCommanderTorpedoExplosionTextures: TextureList = sm.torpedoExplosionTextures

    def setup(self):
        """
        Set up the game here. Call this function to restart the game.
        """
        enterpriseTorpedoExplosion:     EnterpriseTorpedoExplosion     = self._getEnterpriseTorpedoExplosion()
        klingonTorpedoExplosion:        KlingonTorpedoExplosion        = self._getKlingonTorpedoExplosion()
        commanderTorpedoExplosion:      CommanderTorpedoExplosion      = self._getCommanderTorpedoExplosion()
        superCommanderTorpedoExplosion: SuperCommanderTorpedoExplosion = self._getSuperCommanderTorpedoExplosion()

        self._sprites.append(enterpriseTorpedoExplosion)
        self._sprites.append(klingonTorpedoExplosion)
        self._sprites.append(commanderTorpedoExplosion)
        self._sprites.append(superCommanderTorpedoExplosion)

    def on_draw(self):
        """
        Render the screen.
        """
        start_render()
        self._sprites.draw()

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

    def _getEnterpriseTorpedoExplosion(self) -> EnterpriseTorpedoExplosion:

        explosion: EnterpriseTorpedoExplosion = EnterpriseTorpedoExplosion(textureList=self._enterpriseTorpedoExplosionTextures)

        halfScreenWidth:  int = SCREEN_WIDTH // 2
        halfScreenHeight: int = SCREEN_HEIGHT // 2

        explosion.center_x = halfScreenWidth // 2
        explosion.center_y = halfScreenHeight // 2

        return explosion

    def _getKlingonTorpedoExplosion(self) -> KlingonTorpedoExplosion:

        explosion: KlingonTorpedoExplosion = KlingonTorpedoExplosion(textureList=self._klingonTorpedoExplosionTextures)

        halfScreenWidth:  int = SCREEN_WIDTH // 2
        halfScreenHeight: int = SCREEN_HEIGHT // 2

        explosion.center_x = halfScreenWidth  + 200
        explosion.center_y = halfScreenHeight + 200

        return explosion

    def _getCommanderTorpedoExplosion(self) -> CommanderTorpedoExplosion:

        explosion: CommanderTorpedoExplosion = CommanderTorpedoExplosion(textureList=self._commanderTorpedoExplosionTextures)

        halfScreenWidth:  int = SCREEN_WIDTH // 2
        halfScreenHeight: int = SCREEN_HEIGHT // 2

        explosion.center_x = halfScreenWidth  - 200
        explosion.center_y = halfScreenHeight + 200

        return explosion

    def _getSuperCommanderTorpedoExplosion(self) -> SuperCommanderTorpedoExplosion:

        explosion: SuperCommanderTorpedoExplosion = SuperCommanderTorpedoExplosion(textureList=self._superCommanderTorpedoExplosionTextures)

        halfScreenWidth:  int = SCREEN_WIDTH // 2
        halfScreenHeight: int = SCREEN_HEIGHT // 2

        explosion.center_x = halfScreenWidth  + 200
        explosion.center_y = halfScreenHeight - 200

        return explosion


def main():
    """
    Main method
    """
    LocateResources.setupSystemLogging()
    SettingsCommon.determineSettingsLocation()

    window: TestSpriteSheet = TestSpriteSheet(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeRun()


if __name__ == "__main__":
    main()
