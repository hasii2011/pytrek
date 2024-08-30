
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import MOUSE_BUTTON_LEFT
from arcade import Texture

from arcade import load_texture
from arcade import start_render

from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.GameState import GameState

from pytrek.LocateResources import LocateResources

from pytrek.SoundMachine import SoundMachine

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.engine.futures.EventEngine import EventEngine

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.BaseSection import BaseSection
from pytrek.gui.Common import drawQuadrantGrid
from pytrek.gui.MessageConsoleProxy import MessageConsoleProxy

from pytrek.mediators.EnterpriseMediator import EnterpriseMediator
from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings


class QuadrantSection(BaseSection):

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

        self._quadrantMediator:   QuadrantMediator   = QuadrantMediator()

        self._messageConsoleProxy: MessageConsoleProxy = MessageConsoleProxy()
        assert self._messageConsoleProxy.initialized is True, 'The console proxy should have set up at game startup'

        self._eventEngine:  EventEngine  = EventEngine(self._messageConsoleProxy)
        self._soundMachine: SoundMachine = SoundMachine()

        self._enterprise: Enterprise = self._gameState.enterprise

        self._galaxyMediator: GalaxyMediator = GalaxyMediator()
        self._quadrant:       Quadrant       = self._galaxy.currentQuadrant

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=self._enterprise)

        self._enterpriseMediator: EnterpriseMediator = cast(EnterpriseMediator, None)

    def _setEnterpriseMediator(self, newValue: EnterpriseMediator):
        self._enterpriseMediator = newValue
        self._enterpriseMediator.warpTravelCallback = self._enterpriseHasWarped

    # noinspection PyTypeChecker
    enterpriseMediator = property(fget=None, fset=_setEnterpriseMediator, doc='Set by the section UI')

    def on_draw(self):
        """
        Remember arcade's 0,0 origin is lower left corner

        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.

        start_render()

        drawQuadrantGrid(background=self.background)
        self._quadrantMediator.draw(quadrant=self._quadrant)
        self.drawDebug()

    def on_update(self, delta_time: float):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.

        Args:
            delta_time:  Time interval since the last time the function was called.
        """

        self._quadrantMediator.update(quadrant=self._quadrant)
        self._enterpriseMediator.update(quadrant=self._quadrant)

        self._gameEngine.updateRealTimeClock(deltaTime=delta_time)

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        """
        Called when the user presses a mouse button.
        """

        if button == MOUSE_BUTTON_LEFT:
            arcadePoint: ArcadePoint = ArcadePoint(x=x, y=y)
            self.logger.debug(f'{arcadePoint=}')
            if x < QUADRANT_GRID_WIDTH and y >= CONSOLE_SECTION_HEIGHT:
                self._enterpriseMediator.doDeveloperImpulseMove(quadrant=self._quadrant, arcadePoint=arcadePoint)

    def _enterpriseHasWarped(self, destinationCoordinates: Coordinates):

        currentCoordinates: Coordinates = self._quadrant.coordinates

        self._galaxyMediator.doWarp(currentCoordinates=currentCoordinates, destinationCoordinates=destinationCoordinates)
        self._quadrant = self._galaxy.getQuadrant(quadrantCoordinates=destinationCoordinates)
        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=self._enterprise)

