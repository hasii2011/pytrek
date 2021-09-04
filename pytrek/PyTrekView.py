
from typing import cast

from logging import Logger
from logging import getLogger

import arcade
# noinspection PyPackageRequirements
from PIL import ImageFont

# from arcade import PhysicsEngineSimple
from arcade import Sound
from arcade import SpriteList
from arcade import Texture
from arcade import View
from arcade import Window
from arcade import key

from arcade import draw_lrwh_rectangle_textured
from arcade import load_texture
from arcade import start_render

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import FIXED_WIDTH_FONT_FILENAME
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.Constants import SCREEN_HEIGHT

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.ShipCondition import ShipCondition
from pytrek.engine.Intelligence import Intelligence

from pytrek.gui.GalaxyView import GalaxyView
from pytrek.gui.LongRangeSensorScanView import LongRangeSensorScanView
from pytrek.gui.MessageConsole import MessageConsole
from pytrek.gui.StatusConsole import StatusConsole
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.mediators.EnterpriseMediator import EnterpriseMediator

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.QuadrantMediator import QuadrantMediator
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon

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
    MADE_UP_PRETTY_MAIN_NAME:     str = "PyTrek"

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
        self._enterpriseMediator: EnterpriseMediator = cast(EnterpriseMediator, None)

        self._statusConsole:    StatusConsole    = cast(StatusConsole, None)
        self._messageConsole:   MessageConsole   = cast(MessageConsole, None)

        self._soundImpulse:        Sound = cast(Sound, None)

        #
        # I am cheating here because I know arcade use PIL under the covers
        #
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.FONT_RESOURCES_PACKAGE_NAME,
                                                           bareFileName=FIXED_WIDTH_FONT_FILENAME)
        ImageFont.truetype(fqFileName)

    def setup(self):

        SettingsCommon.determineSettingsLocation()

        # self._backgroundSprite: QuadrantBackground = QuadrantBackground()

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='QuadrantBackground.png')
        self.background = load_texture(fqFileName)
        # Create the 'physics engine'
        # self.physicsEngine = PhysicsEngineSimple(self._enterprise, self._hardSpriteList)

        self._enterprise: Enterprise = Enterprise()

        # These singletons are initialized for the first time
        self._gameSettings = GameSettings()     # Be able to read the preferences file
        self._gameState    = GameState()        # Set up the game parameters which uses the above
        self._gameEngine   = GameEngine()       # Then the engine needs to be initialized
        self._intelligence = Intelligence()
        self._computer     = Computer()
        self._galaxy       = Galaxy()           # This essentially finishes initializing most of he game

        self._statusConsole    = StatusConsole(gameView=self)       # UI elements
        self._messageConsole   = MessageConsole()

        # An important mediator
        self._enterpriseMediator = EnterpriseMediator(view=self, warpTravelCallback=self._enterpriseHasWarped)

        self._quadrant: Quadrant = self._galaxy.currentQuadrant

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        # And finally the rest of the UI elements
        self._enterQuadrant()

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
        if pressedKey == arcade.key.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)
        elif pressedKey == key.G:
            galaxyView: GalaxyView = GalaxyView(viewCompleteCallback=self._switchViewBack)
            self.window.show_view(galaxyView)
        elif pressedKey == key.L:
            longRangeSensorView: LongRangeSensorScanView = LongRangeSensorScanView(viewCompleteCallback=self._switchViewBack)
            self.window.show_view(longRangeSensorView)
        elif pressedKey == key.T:
            self._quadrantMediator.fireEnterpriseTorpedoes(self._quadrant)
        elif pressedKey == key.P:
            self._quadrantMediator.firePhasers(self._quadrant)
        elif pressedKey == key.D:
            self._quadrantMediator.dock(self._quadrant)
        elif pressedKey == key.W:
            self._enterpriseMediator.warp()

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
        arcadePoint: ArcadePoint = ArcadePoint(x=x, y=y)
        self._enterpriseMediator.impulse(quadrant=self._quadrant, arcadePoint=arcadePoint)
        # self._quadrantMediator.handleMousePress(quadrant=self._quadrant, arcadePoint=arcadePoint, button=button, keyModifiers=key_modifiers)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def _enterpriseHasWarped(self, warpSpeed: float, destinationCoordinates: Coordinates):

        currentCoordinates: Coordinates = self._quadrant.coordinates
        travelDistance:     float       = self._computer.computeGalacticDistance(startQuadrantCoordinates=currentCoordinates,
                                                                                 endQuadrantCoordinates=destinationCoordinates)
        energyConsumed: float = self._gameEngine.computeEnergyForWarpTravel(travelDistance=travelDistance, warpFactor=warpSpeed)

        self._gameState.energy -= energyConsumed
        self._gameEngine.updateTimeAfterWarpTravel(travelDistance=travelDistance, warpFactor=warpSpeed)

        self.logger.info(f'After warp travel consumed energy: {energyConsumed:.2f}')

        #
        # Cleanup old quadrant
        #
        sectorCoordinates: Coordinates = self._quadrant.enterpriseCoordinates
        oldSector:         Sector      = self._quadrant.getSector(sectorCoordinates=sectorCoordinates)

        oldSector.type   = SectorType.EMPTY
        oldSector.sprite = cast(GamePiece, None)
        #
        # Set up new quadrant
        #
        self._quadrant                             = self._galaxy.getQuadrant(quadrantCoordinates=destinationCoordinates)
        self._galaxy.currentQuadrant               = self._quadrant
        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        self._enterQuadrant()

        self._messageConsole.displayMessage(f"Warped to: {destinationCoordinates} at warp: {warpSpeed}")

    def _enterQuadrant(self):

        currentSectorCoordinates: Coordinates = self._intelligence.generateSectorCoordinates()

        playerList: SpriteList = SpriteList()
        playerList.append(self._enterprise)

        self._gameState.currentSectorCoordinates = currentSectorCoordinates
        self._quadrant.placeEnterprise(self._enterprise, currentSectorCoordinates)

        self._quadrantMediator = QuadrantMediator()

        self._quadrantMediator.playerList = playerList
        # Don't do this until we have setup the current quadrant
        self._makeEnemySpriteLists()
        self._doDebugActions()

    def _switchViewBack(self):
        self.window.show_view(self)

    def _doDebugActions(self):

        self.__doEnemyDebugActions()

        if self._gameSettings.debugAddPlanet is True:
            self._quadrant.addPlanet()

        if self._gameSettings.debugAddStarBase is True:
            self._quadrant.addStarBase()

    def _makeEnemySpriteLists(self):
        """
        Place enemies in the appropriate sprite lists
        Depends on the correct quadrant mediator is in place
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
    """ Main method """
    arcadeWindow: Window     = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    gameView:     PyTrekView = PyTrekView()

    arcadeWindow.set_exclusive_keyboard(exclusive=True)
    arcadeWindow.show_view(gameView)

    gameView.setup()
    arcade.run()


if __name__ == "__main__":
    main()
