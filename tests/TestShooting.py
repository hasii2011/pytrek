"""
Used to test enemies shooting at the Enterprise
"""

from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import MOUSE_BUTTON_LEFT
from arcade import Sprite
from arcade import SpriteList
from arcade import Texture
from arcade import View
from arcade import Window
from arcade import color

from arcade import draw_lrwh_rectangle_textured
from arcade import get_sprites_at_point
from arcade import load_texture
from arcade import set_background_color
from arcade import start_render

from arcade import run as arcadeRun
from arcade import key as arcadeKey

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.ShipCondition import ShipCondition

from pytrek.gui.MessageConsole import MessageConsole
from pytrek.gui.StatusConsole import StatusConsole

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.klingon.Klingon import Klingon
from pytrek.gui.gamepieces.Enterprise import Enterprise

from pytrek.mediators.KlingonTorpedoMediator import KlingonTorpedoMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon

from pytrek.Constants import SCREEN_WIDTH
from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT

from pytrek.LocateResources import LocateResources

from pytrek.GameState import GameState


SCREEN_TITLE:  str = "Test Shooting"


class TestShooting(View):
    """
    Main application class.
    """

    MADE_UP_PRETTY_MAIN_NAME: str = "Test Shooter"

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(TestShooting.MADE_UP_PRETTY_MAIN_NAME)

        set_background_color(color.BLACK)

        self.background:  Texture    = cast(Texture, None)
        self._enterprise: Enterprise = cast(Enterprise, None)

        self._galaxy:       Galaxy       = cast(Galaxy, None)
        self._quadrant:     Quadrant     = cast(Quadrant, None)

        self._quadrantMediator: QuadrantMediator = cast(QuadrantMediator, None)
        self._statusConsole:    StatusConsole    = cast(StatusConsole, None)
        self._messageConsole:   MessageConsole   = cast(MessageConsole, None)

        self._gameState:    GameState    = cast(GameState, None)
        self._gameSettings: GameSettings = cast(GameSettings, None)
        self._gameEngine:   GameEngine   = cast(GameEngine, None)

        self._intelligence: Intelligence = cast(Intelligence, None)
        self._computer:     Computer     = cast(Computer, None)

        self._sprites:     SpriteList = SpriteList()

    def setup(self):
        """
        Set up the game here. Call this function to restart the game.
        """

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='QuadrantBackground.png')
        self.background = load_texture(fqFileName)

        self._galaxy       = Galaxy()
        self._gameState    = GameState()
        self._gameSettings = GameSettings()
        self._gameEngine   = GameEngine()
        self._intelligence = Intelligence()
        self._computer     = Computer()

        self._enterprise: Enterprise = Enterprise()

        self._quadrant: Quadrant = self._galaxy.currentQuadrant

        currentSectorCoordinates: Coordinates = self._intelligence.generateSectorCoordinates()

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates
        self._gameState.currentSectorCoordinates   = currentSectorCoordinates

        self._quadrant.placeEnterprise(self._enterprise, currentSectorCoordinates)

        self._sprites.append(self._enterprise)

        self._quadrantMediator = QuadrantMediator()
        self._statusConsole    = StatusConsole(gameView=self)
        self._messageConsole   = MessageConsole()

        self._quadrantMediator.playerList = self._sprites

        self._makeEnemySpriteLists()

        self.logger.info(f'Setup Complete')

    def on_draw(self):
        """
        Render the screen.
        """
        start_render()
        # Draw the background texture
        draw_lrwh_rectangle_textured(bottom_left_x=1, bottom_left_y=CONSOLE_HEIGHT, width=SCREEN_WIDTH, height=QUADRANT_GRID_HEIGHT, texture=self.background)

        self._quadrantMediator.draw(quadrant=self._quadrant)
        self._statusConsole.draw()
        self._messageConsole.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self._quadrantMediator.update(quadrant=self._quadrant)
        # self._gameEngine.updateRealTimeClock(deltaTime=delta_time)

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
        elif releasedKey == arcadeKey.K:
            self._fireKlingonTorpedo()
        elif releasedKey == arcadeKey.C:
            pass
        elif releasedKey == arcadeKey.S:
            pass

    def on_mouse_press(self, x: float, y: float, button: int, keyModifiers: int):
        """
        Called when the user presses a mouse button.
        """
        print(f'{button=} {keyModifiers=}')
        if button == MOUSE_BUTTON_LEFT and keyModifiers == 0:
            klingon: Klingon = self._quadrant.addKlingon()

            gameCoordinates: Coordinates = self._computer.computeCoordinates(x=x, y=y)
            #
            # Recompute a 'centered' arcade point
            arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(gameCoordinates)
            klingon.gameCoordinates = gameCoordinates
            klingon.center_x = arcadePoint.x
            klingon.center_y = arcadePoint.y

            self._quadrantMediator.klingonList.append(klingon)
        elif button == MOUSE_BUTTON_LEFT and keyModifiers == arcadeKey.MOD_CTRL:
            clickedEnemies: List[Sprite] = get_sprites_at_point(point=(x,y), sprite_list=self._quadrantMediator.klingonList)

            for enemy in clickedEnemies:
                print(f'Delete {enemy}')
                enemy.remove_from_sprite_lists()

        arcadePoint: ArcadePoint = ArcadePoint(x=x, y=y)
        self._quadrantMediator.handleMousePress(quadrant=self._quadrant, arcadePoint=arcadePoint, button=button, keyModifiers=keyModifiers)

    def _fireKlingonTorpedo(self):
        """
        We are testing so we'll access protected methods
        """
        # noinspection PyProtectedMember
        ktm: KlingonTorpedoMediator = self._quadrantMediator._ktm
        for sprite in self._quadrantMediator.klingonList:
            enemy: Enemy = cast(Enemy, sprite)
            # noinspection PyProtectedMember
            ktm._fireTorpedo(enemy=enemy, enterprise=self._enterprise)

    def _makeEnemySpriteLists(self):
        """
        Place enemies in the appropriate sprite lists
        """
        self.__makeKlingonSpriteList()
        self.__makeCommanderSpriteList()
        self.__makeSuperCommanderSpriteList()

    def __makeCommanderSpriteList(self):
        if self._quadrant.commanderCount > 0:
            self._gameState.shipCondition = ShipCondition.Red
            commanderSprites: SpriteList = SpriteList()
            for commander in self._quadrant.commanders:
                commanderSprites.append(commander)

            self._quadrantMediator.commanderList = commanderSprites
        else:
            self._quadrantMediator.commanderList = SpriteList()

    def __makeSuperCommanderSpriteList(self):
        if self._quadrant.superCommanderCount > 0:
            self._gameState.shipCondition = ShipCondition.Red
            superCommanderSprites: SpriteList = SpriteList()
            for superCommander in self._quadrant.superCommanders:
                superCommanderSprites.append(superCommander)

            self._quadrantMediator.superCommanderList = superCommanderSprites
        else:
            self._quadrantMediator.superCommanderList = SpriteList()

    def __makeKlingonSpriteList(self):
        if self._quadrant.klingonCount > 0:
            self._gameState.shipCondition = ShipCondition.Red
            klingonSprites: SpriteList = SpriteList()
            for klingon in self._quadrant.klingons:
                klingonSprites.append(klingon)

            self._quadrantMediator.klingonList = klingonSprites
        else:
            self._quadrantMediator.klingonList = SpriteList()

    def __doEnemyDebugActions(self):

        if self._gameSettings.debugAddKlingons is True:
            numKlingons: int = self._gameSettings.debugKlingonCount
            for x in range(numKlingons):
                self._quadrant.addKlingon()

            self._gameState.remainingKlingons += numKlingons

        if self._gameSettings.debugAddCommanders is True:
            nCommanders: int = self._gameSettings.debugCommanderCount
            for x in range(nCommanders):
                self._quadrant.addCommander()

            self._gameState.remainingCommanders += nCommanders

        if self._gameSettings.debugAddSuperCommanders:
            nSuperCommanders: int = self._gameSettings.debugSuperCommanderCount
            for x in range(nSuperCommanders):
                self._quadrant.addSuperCommander()
            self._gameState.remainingSuperCommanders += nSuperCommanders


def main():
    """
    Main method
    """
    LocateResources.setupSystemLogging()
    SettingsCommon.determineSettingsLocation()

    arcadeWindow: Window     = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    shootingView:     TestShooting = TestShooting()

    arcadeWindow.set_exclusive_keyboard(exclusive=True)
    arcadeWindow.show_view(shootingView)

    shootingView.setup()

    arcadeRun()


if __name__ == "__main__":
    main()
