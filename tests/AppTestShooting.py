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
from arcade import draw_text

from arcade import get_sprites_at_point
from arcade import load_texture
from arcade import set_background_color
from arcade import start_render

from arcade import run as arcadeRun
from arcade import key as arcadeKey
from arcade import exit as arcadeExit

from arcade.color import GRAY
from arcade.color import WHITE

from pytrek.Constants import COMMAND_SECTION_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_NAME
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.Constants import STATUS_VIEW_WIDTH

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.ShipCondition import ShipCondition


from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.gui.gamepieces.base.BaseEnemy import BaseEnemy
from pytrek.gui.gamepieces.base.BaseEnemy import EnemyId
from pytrek.gui.gamepieces.commander.Commander import Commander
from pytrek.gui.gamepieces.klingon.Klingon import Klingon
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.supercommander.SuperCommander import SuperCommander

from pytrek.gui.Common import drawQuadrantGrid

from pytrek.guiv2.MessageConsoleProxy import MessageConsoleProxy
from pytrek.gui.MessageConsoleSection import MessageConsoleSection
from pytrek.guiv2.QuadrantSection import QuadrantSection
from pytrek.gui.StatusConsoleSection import StatusConsoleSection

from pytrek.mediators.CommanderTorpedoMediator import CommanderTorpedoMediator
from pytrek.mediators.EnterpriseMediator import EnterpriseMediator
from pytrek.mediators.EnterprisePhaserMediator import EnterprisePhaserMediator
from pytrek.mediators.KlingonTorpedoMediator import KlingonTorpedoMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator
from pytrek.mediators.SuperCommanderTorpedoMediator import SuperCommanderTorpedoMediator
from pytrek.mediators.base.BaseTorpedoMediator import BaseTorpedoMediator

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings

from pytrek.Constants import SCREEN_WIDTH
from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT

from pytrek.LocateResources import LocateResources

from pytrek.GameState import GameState

from tests.ProjectTestBase import ProjectTestBase

HELP_TEXT1: str = 'Click on sprite to select enemy'
HELP_TEXT2: str = 'Click on quadrant to place'
# noinspection SpellCheckingInspection
HELP_TEXT3: str = 'Q - Fire Torpedo (K)lingon, (C)Commander, (S)uper Commander'

PALETTE_GAME_PIECE_Y: int = 150
HELP_TEXT_X:          int = 16
HELP_TEXT_Y:          int = PALETTE_GAME_PIECE_Y - 48

SCREEN_TITLE:  str = "Test Shooting"


class AppTestShooting(View):
    """
    Main application class.
    """

    MADE_UP_PRETTY_MAIN_NAME: str = "Test Shooter"

    PALETTE_KLINGON_ID:         EnemyId = EnemyId('paletteKlingon')
    PALETTE_COMMANDER_ID:       EnemyId = EnemyId('paletteCommander')
    PALETTE_SUPER_COMMANDER_ID: EnemyId = EnemyId('paletteSuperCommander')

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(AppTestShooting.MADE_UP_PRETTY_MAIN_NAME)

        set_background_color(color.WHITE)

        self.background:  Texture    = cast(Texture, None)
        self._enterprise: Enterprise = cast(Enterprise, None)

        self._galaxy:       Galaxy       = cast(Galaxy, None)
        self._quadrant:     Quadrant     = cast(Quadrant, None)

        self._quadrantMediator:     QuadrantMediator       = cast(QuadrantMediator, None)
        self._statusConsole:        StatusConsoleSection   = cast(StatusConsoleSection, None)
        self._messageConsoleSection: MessageConsoleSection = cast(MessageConsoleSection, None)
        self._messageConsoleProxy:  MessageConsoleProxy    = cast(MessageConsoleProxy, None)
        self._quadrantSection:      QuadrantSection        = cast(QuadrantSection, None)

        self._gameState:    GameState    = cast(GameState, None)
        self._gameSettings: GameSettings = cast(GameSettings, None)
        self._gameEngine:   GameEngine   = cast(GameEngine, None)

        self._intelligence: Intelligence = cast(Intelligence, None)
        self._computer:     Computer     = cast(Computer, None)

        self._sprites:       SpriteList = SpriteList()
        self._staticSprites: SpriteList = SpriteList()

        self._selectedGamePiece: GamePiece = cast(GamePiece, None)

        self._enterpriseMediator: EnterpriseMediator = cast(EnterpriseMediator, None)

    def setup(self):
        """
        Set up the game here. Call this function to restart the game.
        """
        fqFileName: str = LocateResources.getImagePath(bareFileName='QuadrantBackground.png')
        self.background = load_texture(fqFileName)

        self._gameSettings = GameSettings()
        self._gameState    = GameState()
        self._gameEngine   = GameEngine()
        self._intelligence = Intelligence()
        self._computer     = Computer()
        self._galaxy       = Galaxy()

        self._enterprise = self._gameState.enterprise
        self._quadrant   = self._galaxy.currentQuadrant

        self._quadrant.klingonCount        = 0
        self._quadrant.commanderCount      = 0
        self._quadrant.superCommanderCount = 0

        currentSectorCoordinates: Coordinates = self._intelligence.generateSectorCoordinates()

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates
        self._gameState.currentSectorCoordinates   = currentSectorCoordinates

        self._messageConsoleSection = MessageConsoleSection(left=0,
                                                            bottom=COMMAND_SECTION_HEIGHT,
                                                            height=CONSOLE_SECTION_HEIGHT,
                                                            width=SCREEN_WIDTH,
                                                            accept_keyboard_events=True
                                                            )

        self._messageConsoleProxy = MessageConsoleProxy()
        self._messageConsoleProxy.console = self._messageConsoleSection

        self._statusConsole = StatusConsoleSection(left=QUADRANT_GRID_WIDTH,
                                                   bottom=SCREEN_HEIGHT - QUADRANT_GRID_HEIGHT,
                                                   height=QUADRANT_GRID_HEIGHT + CONSOLE_SECTION_HEIGHT, width=STATUS_VIEW_WIDTH,
                                                   accept_keyboard_events=True)

        self._quadrantSection = QuadrantSection(left=0,
                                                bottom=SCREEN_HEIGHT - QUADRANT_GRID_HEIGHT,
                                                height=QUADRANT_GRID_HEIGHT, width=QUADRANT_GRID_WIDTH,
                                                accept_keyboard_events=True)

        self.section_manager.add_section(self._quadrantSection)
        self.section_manager.add_section(self._statusConsole)
        self.section_manager.add_section(self._messageConsoleSection)

        self._quadrantMediator   = QuadrantMediator()

        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=self._enterprise)

        self._enterpriseMediator = EnterpriseMediator(view=self, warpTravelCallback=self._noOp)

        self._makeEnemySpriteLists()

        self._makeGamePiecePalette()
        self.logger.info(f'Setup Complete')

    def on_draw(self):
        """
        Render the screen.
        """
        start_render()
        drawQuadrantGrid(background=self.background)

        self._quadrantMediator.draw(quadrant=self._quadrant)
        self._staticSprites.draw()
        self._drawInstructions()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self._quadrantMediator.update(quadrant=self._quadrant)
        self._enterpriseMediator.update(quadrant=self._quadrant)

    def on_key_release(self, releasedKey: int, key_modifiers: int):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if releasedKey == arcadeKey.Q:
            arcadeExit()
        elif releasedKey == arcadeKey.A:
            self.setup()
        elif releasedKey == arcadeKey.K:
            self._fireKlingonTorpedo()
        elif releasedKey == arcadeKey.C:
            self._fireCommanderTorpedo()
        elif releasedKey == arcadeKey.S:
            self._fireSuperCommanderTorpedo()
        elif releasedKey == arcadeKey.P:
            self._firePhasers()

    def on_mouse_release(self, x: float, y: float, button: int, keyModifiers: int):
        """
        Called when the user presses a mouse button.
        """
        self.logger.info(f'{button=} {keyModifiers=}')
        if button == MOUSE_BUTTON_LEFT and keyModifiers == arcadeKey.MOD_CTRL:
            # Try klingons first
            clickedEnemies: List[Sprite] = get_sprites_at_point(point=(x, y), sprite_list=self._quadrantMediator.klingonList)

            # The Commanders
            if len(clickedEnemies) == 0:
                clickedEnemies = get_sprites_at_point(point=(x, y), sprite_list=self._quadrantMediator.commanderList)

            # Must be Super Commanders
            if len(clickedEnemies) == 0:
                clickedEnemies = get_sprites_at_point(point=(x, y), sprite_list=self._quadrantMediator.superCommanderList)

            for enemy in clickedEnemies:
                self.logger.info(f'Delete {enemy}')
                enemy.remove_from_sprite_lists()
        elif button == MOUSE_BUTTON_LEFT:

            if self._selectedGamePiece is None:
                clickedPaletteSprites: List[Sprite] = get_sprites_at_point(point=(x, y), sprite_list=self._staticSprites)

                for paletteSprite in clickedPaletteSprites:
                    paletteSprite.color = color.BLACK
                    self._selectedGamePiece = paletteSprite
            else:
                # A palette sprite is selected
                self._placeSpriteOnBoard(x=x, y=y)

                self.logger.info(f'Clear selected Sprite')
                self._selectedGamePiece.color = color.WHITE
                self._selectedGamePiece       = cast(GamePiece, None)

        arcadePoint: ArcadePoint = ArcadePoint(x=x, y=y)
        self._quadrantMediator.handleMousePress(quadrant=self._quadrant, arcadePoint=arcadePoint, button=button, keyModifiers=keyModifiers)

    def _placeSpriteOnBoard(self, x: float, y: float):

        enemy: BaseEnemy = cast(BaseEnemy, self._selectedGamePiece)

        if enemy.id == AppTestShooting.PALETTE_KLINGON_ID:
            klingon: Klingon = self._quadrant.addKlingon()
            added: bool = self._addEnemyToTestGrid(enemy=klingon, x=x, y=y)
            if added is True:
                self._quadrantMediator.klingonList.append(klingon)
        elif enemy.id == AppTestShooting.PALETTE_COMMANDER_ID:
            commander: Commander = self._quadrant.addCommander()
            added = self._addEnemyToTestGrid(enemy=commander, x=x, y=y)
            if added is True:
                self._quadrantMediator.commanderList.append(commander)

        elif enemy.id == AppTestShooting.PALETTE_SUPER_COMMANDER_ID:
            superCommander: SuperCommander = self._quadrant.addSuperCommander()
            added = self._addEnemyToTestGrid(enemy=superCommander, x=x, y=y)
            if added is True:
                self._quadrantMediator.superCommanderList.append(superCommander)

    def _fireKlingonTorpedo(self):
        """
        We are testing so we'll access protected methods
        """
        # noinspection PyProtectedMember
        ktm: KlingonTorpedoMediator = self._quadrantMediator._ktm
        self.__fireEnemyTorpedo(torpedoMediator=ktm, enemySprites=self._quadrantMediator.klingonList, rotationAngle=Klingon.ROTATION_ANGLE)

    def _fireCommanderTorpedo(self):
        """
        We are testing so we'll access protected methods
        """
        # noinspection PyProtectedMember
        ctm: CommanderTorpedoMediator = self._quadrantMediator._ctm
        self.__fireEnemyTorpedo(torpedoMediator=ctm, enemySprites=self._quadrantMediator.commanderList, rotationAngle=Commander.ROTATION_ANGLE)

    def _fireSuperCommanderTorpedo(self):
        """
        We are testing so we'll access protected methods
        """
        # noinspection PyProtectedMember
        stm: SuperCommanderTorpedoMediator = self._quadrantMediator._stm
        self.__fireEnemyTorpedo(torpedoMediator=stm, enemySprites=self._quadrantMediator.superCommanderList, rotationAngle=SuperCommander.ROTATION_ANGLE)

    def _firePhasers(self):

        # noinspection PyProtectedMember
        epm: EnterprisePhaserMediator = self._quadrantMediator._epm

        epm.firePhasers(quadrant=self._quadrant)

    # noinspection PyUnusedLocal
    def _noOp(self, destinationCoordinates: Coordinates) -> None:
        self.logger.warning(f'******** How did we warp? *************')

    def __fireEnemyTorpedo(self, torpedoMediator: BaseTorpedoMediator, enemySprites: SpriteList, rotationAngle: int = 0):

        for sprite in enemySprites:
            enemy: Enemy = cast(Enemy, sprite)
            # noinspection PyProtectedMember
            torpedoMediator._pointAtEnterprise(enemy=enemy, enterprise=self._enterprise, rotationAngle=rotationAngle)
            # noinspection PyProtectedMember
            torpedoMediator._fireTorpedo(enemy=enemy, enterprise=self._enterprise)

    def _makeEnemySpriteLists(self):
        """
        Place enemies in the appropriate sprite lists
        """
        self.__makeKlingonSpriteList()
        self.__makeCommanderSpriteList()
        self.__makeSuperCommanderSpriteList()

    def _makeGamePiecePalette(self):
        """
        These are the static icons that can be dragged on screen

        """
        bogusCoordinates: Coordinates = Coordinates(-1, -1)
        paletteKlingon: Klingon = Klingon(coordinates=bogusCoordinates)
        paletteKlingon.id = AppTestShooting.PALETTE_KLINGON_ID
        paletteKlingon.center_x = 32
        paletteKlingon.center_y = PALETTE_GAME_PIECE_Y

        paletteCommander: Commander = Commander(coordinates=bogusCoordinates, moveInterval=-1)
        paletteCommander.id = AppTestShooting.PALETTE_COMMANDER_ID
        paletteCommander.center_x = paletteKlingon.center_x + 64
        paletteCommander.center_y = PALETTE_GAME_PIECE_Y

        paletteSuperCommander: SuperCommander = SuperCommander(coordinates=bogusCoordinates, moveInterval=-1)
        paletteSuperCommander.id = AppTestShooting.PALETTE_SUPER_COMMANDER_ID
        paletteSuperCommander.center_x = paletteCommander.center_x + 64
        paletteSuperCommander.center_y = PALETTE_GAME_PIECE_Y

        self._staticSprites.append(paletteKlingon)
        self._staticSprites.append(paletteCommander)
        self._staticSprites.append(paletteSuperCommander)

    def _drawInstructions(self):

        draw_text(HELP_TEXT1, HELP_TEXT_X, HELP_TEXT_Y,      color=WHITE, font_size=12, font_name=FIXED_WIDTH_FONT_NAME)
        draw_text(HELP_TEXT2, HELP_TEXT_X, HELP_TEXT_Y - 16, color=WHITE, font_size=12, font_name=FIXED_WIDTH_FONT_NAME)
        draw_text(HELP_TEXT3, HELP_TEXT_X, HELP_TEXT_Y - 32, color=WHITE, font_size=12, font_name=FIXED_WIDTH_FONT_NAME)

    def _addEnemyToTestGrid(self, enemy: BaseEnemy, x: float, y: float,) -> bool:

        added: bool = True
        gameCoordinates: Coordinates = self._computer.computeCoordinates(x=x, y=y)
        if gameCoordinates.valid() is True:
            # Recompute a 'centered' arcade point
            arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(gameCoordinates)

            enemy.gameCoordinates = gameCoordinates
            enemy.center_x = arcadePoint.x
            enemy.center_y = arcadePoint.y
        else:
            added = False

        return added

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

        if self._gameSettings.addKlingons is True:
            numKlingons: int = self._gameSettings.klingonCount
            for x in range(numKlingons):
                self._quadrant.addKlingon()

            self._gameState.remainingKlingons += numKlingons

        if self._gameSettings.addCommanders is True:
            nCommanders: int = self._gameSettings.commanderCount
            for x in range(nCommanders):
                self._quadrant.addCommander()

            self._gameState.remainingCommanders += nCommanders

        if self._gameSettings.addSuperCommanders:
            nSuperCommanders: int = self._gameSettings.superCommanderCount
            for x in range(nSuperCommanders):
                self._quadrant.addSuperCommander()
            self._gameState.remainingSuperCommanders += nSuperCommanders


def main():
    """
    Main method
    """
    ProjectTestBase.setUpLogging()

    arcadeWindow: Window          = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    shootingView: AppTestShooting = AppTestShooting()

    arcadeWindow.background_color = GRAY
    arcadeWindow.set_exclusive_keyboard(exclusive=True)
    arcadeWindow.show_view(shootingView)

    shootingView.setup()

    arcadeRun()


if __name__ == "__main__":
    main()
