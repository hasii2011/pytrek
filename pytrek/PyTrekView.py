from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

import logging.config

import os

from json import load as jsonLoad

from PIL import ImageFont

import arcade

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
from pytrek.Constants import SOUND_VOLUME_HIGH

from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.ShipCondition import ShipCondition
from pytrek.engine.Intelligence import Intelligence

from pytrek.gui.GalaxyView import GalaxyView
from pytrek.gui.LongRangeSensorScanView import LongRangeSensorScanView
from pytrek.gui.MessageConsole import MessageConsole
from pytrek.gui.StatusConsole import StatusConsole
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.ExplosionColor import ExplosionColor

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.QuadrantMediator import QuadrantMediator

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

        self._setupSystemLogging()

        super().__init__()

        self.logger: Logger = getLogger(PyTrekView.MADE_UP_PRETTY_MAIN_NAME)

        self.background:  Texture    = cast(Texture, None)
        self._enterprise: Enterprise = cast(Enterprise, None)
        # If you have sprite lists, you should create them here and set them to None
        # self.physicsEngine: PhysicsEnginePlatformer = cast(PhysicsEnginePlatformer, None)
        # self.physicsEngine: PhysicsEngineSimple = cast(PhysicsEngineSimple, None)

        self._intelligence: Intelligence = cast(Intelligence, None)
        self._computer:     Computer     = cast(Computer, None)
        self._gameEngine:   GameEngine   = cast(GameEngine, None)
        self._gameState:    GameState    = cast(GameState, None)
        self._gameSettings: GameSettings = cast(GameSettings, None)

        self._galaxy:       Galaxy       = cast(Galaxy, None)
        self._quadrant:     Quadrant     = cast(Quadrant, None)

        self._quadrantMediator:      QuadrantMediator      = cast(QuadrantMediator, None)
        self._statusConsole:    StatusConsole    = cast(StatusConsole, None)
        self._messageConsole:   MessageConsole   = cast(MessageConsole, None)

        self._soundImpulse:        Sound = cast(Sound, None)

        self._photonTorpedoExplosions: List[Texture] = cast(List[Texture], None)
        #
        # I am cheating here because I know arcade use PIL under the covers
        #
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.FONT_RESOURCES_PACKAGE_NAME, bareFileName=FIXED_WIDTH_FONT_FILENAME)
        ImageFont.truetype(fqFileName)

    def setup(self):

        SettingsCommon.determineSettingsLocation()

        # self._backgroundSprite: QuadrantBackground = QuadrantBackground()

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='QuadrantBackground.png')
        self.background = load_texture(fqFileName)
        # Create the 'physics engine'
        # self.physicsEngine = PhysicsEnginePlatformer(self.enterprise, self.hardSpriteList, gravity_constant=GRAVITY)
        # self.physicsEngine = PhysicsEngineSimple(self._enterprise, self._hardSpriteList)

        self._enterprise: Enterprise = Enterprise()

        self._intelligence = Intelligence()
        self._computer     = Computer()
        self._gameEngine   = GameEngine()
        self._gameState    = GameState()
        self._gameSettings = GameSettings()

        self._galaxy       = Galaxy()

        self._quadrant: Quadrant = self._galaxy.currentQuadrant

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates
        currentSectorCoordinates: Coordinates = self._intelligence.generateSectorCoordinates()

        playerList: SpriteList = SpriteList()
        playerList.append(self._enterprise)

        self._gameState.currentSectorCoordinates = currentSectorCoordinates
        self._quadrant.placeEnterprise(self._enterprise, currentSectorCoordinates)

        self._quadrantMediator = QuadrantMediator()
        self._statusConsole    = StatusConsole(gameView=self)
        self._messageConsole   = MessageConsole()

        self._quadrantMediator.playerList       = playerList

        if self._gameSettings.debugAddKlingons is True:
            for x in range(self._gameSettings.debugAddKlingons + 1):
                self._quadrant.addKlingon()

        if self._quadrant.klingonCount > 0:
            self._gameState.shipCondition = ShipCondition.Red
            klingonSprites: SpriteList = SpriteList()
            for klingon in self._quadrant._klingons:
                klingonSprites.append(klingon)

            self._quadrantMediator.klingonList = klingonSprites
        else:
            self._quadrantMediator.klingonList = SpriteList()

        if self._gameSettings.debugAddPlanet is True:
            self._quadrant.addPlanet()
        self._loadSounds()
        self._photonTorpedoExplosions = self._loadPhotonTorpedoExplosions()

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
        self._gameEngine.updateRealTimeClock(deltaTime=delta_time)

    def on_key_press(self, pressedKey, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://arcade.academy/arcade.key.html
        """
        if pressedKey == arcade.key.UP:
            self._enterprise.change_y = MOVEMENT_SPEED
        elif pressedKey == arcade.key.DOWN:
            self._enterprise.change_y = -MOVEMENT_SPEED
        elif pressedKey == arcade.key.LEFT:
            self._enterprise.change_x = -MOVEMENT_SPEED
        elif pressedKey == arcade.key.RIGHT:
            self._enterprise.change_x = MOVEMENT_SPEED
        elif pressedKey == arcade.key.Q:
            # noinspection PyUnresolvedReferences
            os._exit(0)
        elif pressedKey == arcade.key.G:
            galaxyView: GalaxyView = GalaxyView(viewCompleteCallback=self._switchViewBack)
            self.window.show_view(galaxyView)
        elif pressedKey == arcade.key.L:
            longRangeSensorView: LongRangeSensorScanView = LongRangeSensorScanView(viewCompleteCallback=self._switchViewBack)
            self.window.show_view(longRangeSensorView)
        elif pressedKey == arcade.key.T:
            self._quadrantMediator.fireEnterpriseTorpedoesAtKlingons(self._quadrant)

    def on_key_release(self, releasedKey, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if releasedKey == key.LEFT or releasedKey == key.A:
            self._enterprise.change_x = 0
        elif releasedKey == key.RIGHT or releasedKey == key.D:
            self._enterprise.change_x = 0
        elif releasedKey == key.UP or releasedKey == key.W:
            self._enterprise.change_y = 0
        elif releasedKey == key.DOWN or releasedKey == key.X:
            self._enterprise.change_y = 0

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass
        # print(f'Mouse ({x},{y})')

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_RIGHT:
            coordinates: Coordinates = self._computer.computeSectorCoordinates(x=round(x), y=round(y))

            self._quadrant.enterprise.inMotion = True
            self._quadrant.enterpriseCoordinates = coordinates
            self._gameEngine.impulse(newCoordinates=coordinates, quadrant=self._quadrant, enterprise=self._enterprise)
            self._soundImpulse.play(volume=SOUND_VOLUME_HIGH)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def _setupSystemLogging(self):
        configFilePath: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.RESOURCES_PACKAGE_NAME,
                                                               bareFileName=LocateResources.JSON_LOGGING_CONFIG_FILENAME)

        with open(configFilePath, 'r') as loggingConfigurationFile:
            configurationDictionary = jsonLoad(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads   = False

    def _loadSounds(self):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName='probe_launch_1.wav')
        self._soundImpulse = Sound(file_name=fqFileName)

    def _loadPhotonTorpedoExplosions(self) -> List[Texture]:

        explosions: List[Texture] = []

        for eColor in ExplosionColor:
            bareFileName: str = f'explosion_rays_{eColor.value}.png'
            fqFileName:   str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

            explosion = load_texture(fqFileName)
            explosions.append(explosion)

        return explosions

    def _switchViewBack(self):
        self.window.show_view(self)


def main():
    """ Main method """
    arcadeWindow: Window     = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    gameView:     PyTrekView = PyTrekView()

    arcadeWindow.show_view(gameView)

    gameView.setup()
    arcade.run()


if __name__ == "__main__":
    main()
