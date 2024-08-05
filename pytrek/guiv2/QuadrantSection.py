
from logging import Logger
from logging import getLogger

from arcade import MOUSE_BUTTON_LEFT
from arcade import Section
from arcade import Texture

from arcade import draw_lrwh_rectangle_textured
from arcade import load_texture
from arcade import start_render

from arcade import key as arcadeKey
from arcade import exit as arcadeExit

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.Constants import SCREEN_WIDTH
from pytrek.GameState import GameState

from pytrek.LocateResources import LocateResources

from pytrek.SoundMachine import SoundMachine

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.engine.futures.EventEngine import EventEngine

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.guiv2.MessageConsoleProxy import MessageConsoleProxy

from pytrek.mediators.EnterpriseMediator import EnterpriseMediator
from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings


class QuadrantSection(Section):

    def __init__(self, left: int, bottom: int, width: int, height: int, **kwargs):
        self.logger: Logger = getLogger(__name__)

        super().__init__(left, bottom, width, height, **kwargs)

        fqFileName:      str     = LocateResources.getImagePath(bareFileName='QuadrantBackground.png')
        self.background: Texture = load_texture(fqFileName)

        self._gameSettings: GameSettings = GameSettings()     # Be able to read the preferences file
        self._gameState:    GameState    = GameState()        # Set up the game parameters which uses the above
        self._gameEngine:   GameEngine   = GameEngine()       # Then the engine needs to be initialized
        self._intelligence: Intelligence = Intelligence()
        self._computer:     Computer     = Computer()
        self._galaxy:       Galaxy       = Galaxy()           # This essentially finishes initializing most of the game

        self._enterpriseMediator: EnterpriseMediator = EnterpriseMediator(view=self, warpTravelCallback=self._enterpriseHasWarped)
        self._quadrantMediator:   QuadrantMediator   = QuadrantMediator()

        assert MessageConsoleProxy().initialized is True, 'The console proxy should have set up at game startup'
        self._eventEngine:  EventEngine  = EventEngine(MessageConsoleProxy())
        self._soundMachine: SoundMachine = SoundMachine()

        self._enterprise: Enterprise = self._gameState.enterprise

        # Important mediators
        self._galaxyMediator: GalaxyMediator = GalaxyMediator()
        self._quadrant:       Quadrant       = self._galaxy.currentQuadrant

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        # And finally the rest of the UI elements
        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=self._enterprise)

        self._freezeGamePlay: bool = False      # used to temporarily stop game while a dialog is popped up

    def on_draw(self):
        """
        Remember arcade's 0,0 origin is lower left corner

        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.

        start_render()

        # Draw the background texture
        draw_lrwh_rectangle_textured(bottom_left_x=1, bottom_left_y=CONSOLE_HEIGHT,
                                     width=SCREEN_WIDTH, height=QUADRANT_GRID_HEIGHT, texture=self.background)

        self._quadrantMediator.draw(quadrant=self._quadrant)

    def on_update(self, delta_time: float):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.

        Args:
            delta_time:  Time interval since the last time the function was called.
        """
        if self._freezeGamePlay is True:
            return

        self._quadrantMediator.update(quadrant=self._quadrant)
        self._enterpriseMediator.update(quadrant=self._quadrant)

        self._gameEngine.updateRealTimeClock(deltaTime=delta_time)

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        """
        Called when the user presses a mouse button.
        """
        if self._freezeGamePlay is True:
            return

        if button == MOUSE_BUTTON_LEFT:
            arcadePoint: ArcadePoint = ArcadePoint(x=x, y=y)
            self.logger.warning(f'{arcadePoint=}')
            if x < QUADRANT_GRID_WIDTH and y >= CONSOLE_HEIGHT:
                self._enterpriseMediator.impulse(quadrant=self._quadrant, arcadePoint=arcadePoint)

    def on_key_press(self, pressedKey: int, modifiers: int):

        match pressedKey:
            case arcadeKey.Q:
                arcadeExit()
            case arcadeKey.P:
                self._quadrantMediator.firePhasers(self._quadrant)
                self._gameEngine.resetOperationTime()
            case arcadeKey.T:
                self._quadrantMediator.fireEnterpriseTorpedoes(self._quadrant)
                self._gameEngine.resetOperationTime()
            case arcadeKey.W:
                self._enterpriseMediator.warp()

    def _enterpriseHasWarped(self, warpSpeed: float, destinationCoordinates: Coordinates):

        currentCoordinates: Coordinates = self._quadrant.coordinates

        self._galaxyMediator.doWarp(currentCoordinates=currentCoordinates, destinationCoordinates=destinationCoordinates, warpSpeed=warpSpeed)
        self._quadrant = self._galaxy.getQuadrant(quadrantCoordinates=destinationCoordinates)
        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=self._enterprise)

        # self._messageConsole.displayMessage(f"Warped to: {destinationCoordinates} at warp: {warpSpeed}")
