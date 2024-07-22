
from typing import cast

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from PIL import ImageFont

from arcade import MOUSE_BUTTON_LEFT

from arcade import Texture
from arcade import View
from arcade import Window

from arcade import draw_lrwh_rectangle_textured
from arcade import load_texture
from arcade import start_render

from arcade import key as arcadeKey
from arcade import run as arcadeRun

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_FILENAME
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.Constants import SCREEN_WIDTH
from pytrek.Constants import SCREEN_HEIGHT

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.engine.futures.EventEngine import EventEngine

from pytrek.gui.GalaxyView import GalaxyView
from pytrek.gui.HelpView import HelpView
from pytrek.gui.LongRangeSensorScanView import LongRangeSensorScanView
from pytrek.gui.MessageConsole import MessageConsole
from pytrek.gui.StatusConsole import StatusConsole

from pytrek.gui.gamepieces.Enterprise import Enterprise

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.EnterpriseMediator import EnterpriseMediator
from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.settings.GameSettings import GameSettings

from pytrek.SoundMachine import SoundMachine

from pytrek.GameState import GameState

from pytrek.LocateResources import LocateResources

SCREEN_TITLE:  str = "PyTrek"
GRAVITY:       int = 0          # We do not want our game pieces falling

MOVEMENT_SPEED: int = 2


class PyTrekView(View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """
    MADE_UP_PRETTY_MAIN_NAME:     str = "PyTrekView"

    def __init__(self):

        LocateResources.setupSystemLogging()

        super().__init__()

        self.logger: Logger = getLogger(PyTrekView.MADE_UP_PRETTY_MAIN_NAME)

        self.background:  Texture    = cast(Texture, None)
        self._enterprise: Enterprise = cast(Enterprise, None)
        # If you have sprite lists, you should create them here and set them to None
        # self.physicsEngine: PhysicsEngineSimple = cast(PhysicsEngineSimple, None)

        self._intelligence: Intelligence = cast(Intelligence, None)
        self._computer:     Computer     = cast(Computer, None)
        self._gameEngine:   GameEngine   = cast(GameEngine, None)
        self._gameState:    GameState    = cast(GameState, None)
        self._gameSettings: GameSettings = cast(GameSettings, None)

        self._galaxy:       Galaxy       = cast(Galaxy, None)
        self._quadrant:     Quadrant     = cast(Quadrant, None)

        self._quadrantMediator:   QuadrantMediator   = cast(QuadrantMediator, None)
        self._galaxyMediator:     GalaxyMediator     = cast(GalaxyMediator, None)
        self._enterpriseMediator: EnterpriseMediator = cast(EnterpriseMediator, None)

        self._statusConsole:    StatusConsole    = cast(StatusConsole, None)
        self._messageConsole:   MessageConsole   = cast(MessageConsole, None)

        self._soundMachine:     SoundMachine     = cast(SoundMachine, None)

        self._eventEngine: EventEngine = cast(EventEngine, None)
        #
        # I am cheating here because I know arcade use PIL under the covers
        #
        fqFileName: str = LocateResources.getResourcesPath(bareFileName=FIXED_WIDTH_FONT_FILENAME,
                                                           resourcePath=LocateResources.FONT_RESOURCES_PATH,
                                                           packageName=LocateResources.FONT_RESOURCES_PACKAGE_NAME,
                                                           )
        ImageFont.truetype(fqFileName)

    def setup(self):

        # self._backgroundSprite: QuadrantBackground = QuadrantBackground()

        fqFileName: str = LocateResources.getImagePath(bareFileName='QuadrantBackground.png')
        self.background = load_texture(fqFileName)
        # Create the 'physics engine'
        # self.physicsEngine = PhysicsEngineSimple(self._enterprise, self._hardSpriteList)

        # These singletons are initialized for the first time
        self._gameSettings = GameSettings()     # Be able to read the preferences file
        self._gameState    = GameState()        # Set up the game parameters which uses the above
        self._gameEngine   = GameEngine()       # Then the engine needs to be initialized
        self._intelligence = Intelligence()
        self._computer     = Computer()
        self._galaxy       = Galaxy()           # This essentially finishes initializing most of the game

        self._messageConsole = MessageConsole()
        self._eventEngine    = EventEngine(self._messageConsole)

        self._statusConsole = StatusConsole(gameView=self)       # UI elements
        self._soundMachine  = SoundMachine()

        self._enterprise = self._gameState.enterprise

        # Important mediators
        self._enterpriseMediator = EnterpriseMediator(view=self, warpTravelCallback=self._enterpriseHasWarped)
        self._quadrantMediator   = QuadrantMediator()
        self._galaxyMediator     = GalaxyMediator()
        self._quadrant           = self._galaxy.currentQuadrant

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        # And finally the rest of the UI elements
        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=self._enterprise)

        self.logger.info(f'{self._enterprise=}')
        self.logger.info(f'{self._quadrant=}')
        self.logger.info(f'Setup Complete')

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        start_render()

        # Draw the background texture
        draw_lrwh_rectangle_textured(bottom_left_x=1, bottom_left_y=CONSOLE_HEIGHT,
                                     width=SCREEN_WIDTH, height=QUADRANT_GRID_HEIGHT, texture=self.background)

        # Call draw() on all our sprite lists
        self._quadrantMediator.draw(quadrant=self._quadrant)
        self._statusConsole.draw()
        self._messageConsole.draw()

    def on_update(self, delta_time: float):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.

        Args:
            delta_time:  Time interval since the last time the function was called.
        """
        # self.physicsEngine.update()
        self._quadrantMediator.update(quadrant=self._quadrant)
        self._enterpriseMediator.update(quadrant=self._quadrant)

        self._gameEngine.updateRealTimeClock(deltaTime=delta_time)

    def on_key_press(self, pressedKey: int, key_modifiers: int):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://arcade.academy/arcade.key.html
        """
        if pressedKey == arcadeKey.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)
        elif pressedKey == arcadeKey.G:
            galaxyView: GalaxyView = GalaxyView(viewCompleteCallback=self._switchViewBack)
            self.window.show_view(galaxyView)
            self._gameEngine.resetOperationTime()
        elif pressedKey == arcadeKey.L:
            longRangeSensorView: LongRangeSensorScanView = LongRangeSensorScanView(viewCompleteCallback=self._switchViewBack)
            self.window.show_view(longRangeSensorView)
            self._gameEngine.resetOperationTime()
        elif pressedKey == arcadeKey.T:
            self._quadrantMediator.fireEnterpriseTorpedoes(self._quadrant)
            self._gameEngine.resetOperationTime()
        elif pressedKey == arcadeKey.P:
            self._quadrantMediator.firePhasers(self._quadrant)
            self._gameEngine.resetOperationTime()
        elif pressedKey == arcadeKey.D:
            self._quadrantMediator.dock(self._quadrant)
            self._gameEngine.resetOperationTime()
        elif pressedKey == arcadeKey.W:
            self._enterpriseMediator.warp()
        elif pressedKey == arcadeKey.H or pressedKey == arcadeKey.QUESTION:
            print('Asked for help!')
            self._displayHelp()

    def on_mouse_motion(self, x: float, y: float, delta_x: float, delta_y: float):
        """
        Called whenever the mouse moves.
        """
        pass
        # print(f'Mouse ({x},{y})')

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        """
        Called when the user presses a mouse button.
        """
        if button == MOUSE_BUTTON_LEFT:
            arcadePoint: ArcadePoint = ArcadePoint(x=x, y=y)
            if x < QUADRANT_GRID_WIDTH and y >= CONSOLE_HEIGHT:
                self._enterpriseMediator.impulse(quadrant=self._quadrant, arcadePoint=arcadePoint)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def _enterpriseHasWarped(self, warpSpeed: float, destinationCoordinates: Coordinates):

        currentCoordinates: Coordinates = self._quadrant.coordinates

        self._galaxyMediator.doWarp(currentCoordinates=currentCoordinates, destinationCoordinates=destinationCoordinates,
                                    warpSpeed=warpSpeed)
        self._quadrant = self._galaxy.getQuadrant(quadrantCoordinates=destinationCoordinates)
        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=self._enterprise)

        self._messageConsole.displayMessage(f"Warped to: {destinationCoordinates} at warp: {warpSpeed}")

    def _displayHelp(self):

        helpView: HelpView = HelpView(completeCallback=self._switchViewBack)

        self.window.show_view(helpView)

    def _switchViewBack(self):
        self.window.show_view(self)


def main():
    """ Main method """
    arcadeWindow: Window     = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    gameView:     PyTrekView = PyTrekView()

    arcadeWindow.set_exclusive_keyboard(exclusive=False)
    arcadeWindow.show_view(gameView)

    gameView.setup()
    arcadeRun()


if __name__ == "__main__":
    main()
