
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

import logging.config

from json import load as jsonLoad

import arcade

from arcade import PhysicsEngineSimple
from arcade import SpriteList
from arcade import Texture
from arcade import View
from arcade import Window

from arcade import key

from arcade import draw_lrwh_rectangle_textured
from arcade import load_texture
from arcade import start_render

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.Constants import SCREEN_HEIGHT
from pytrek.engine.Computer import Computer

from pytrek.gui.gamepieces.Enterprise import Enterprise

from pytrek.LocateResources import LocateResources

from pytrek.engine.Intelligence import Intelligence

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.mediators.QuadrantMediator import QuadrantMediator
from pytrek.settings.SettingsCommon import SettingsCommon

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

        # set_background_color(color.LIGHT_GRAY)
        # self._backgroundSprite: QuadrantBackground = cast(QuadrantBackground, None)
        self.background:  Texture    = cast(Texture, None)
        self._enterprise: Enterprise = cast(Enterprise, None)
        # If you have sprite lists, you should create them here,
        # and set them to None

        # self.physicsEngine: PhysicsEnginePlatformer = cast(PhysicsEnginePlatformer, None)
        self.physicsEngine: PhysicsEngineSimple = cast(PhysicsEngineSimple, None)

        self._intelligence: Intelligence = cast(Intelligence, None)
        self._computer:     Computer     = cast(Computer, None)
        self._galaxy:       Galaxy       = cast(Galaxy, None)
        self._quadrant:     Quadrant     = cast(Quadrant, None)

    def setup(self):

        SettingsCommon.determineSettingsLocation()

        # self._backgroundSprite: QuadrantBackground = QuadrantBackground()

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='QuadrantBackground.png')
        self.background = load_texture(fqFileName)
        # Create the 'physics engine'
        # self.physicsEngine = PhysicsEnginePlatformer(self.enterprise, self.hardSpriteList, gravity_constant=GRAVITY)

        self._enterprise: Enterprise = Enterprise()
        self._hardSpriteList: SpriteList = SpriteList()
        self.physicsEngine = PhysicsEngineSimple(self._enterprise, self._hardSpriteList)

        self._intelligence = Intelligence()
        self._computer     = Computer()
        self._galaxy       = Galaxy()

        self._quadrant: Quadrant = self._galaxy.currentQuadrant

        # self.statistics.currentQuadrantCoordinates = self.galaxy.currentQuadrant.coordinates
        # self.statistics.currentSectorCoordinates   = self.intelligence.getRandomSectorCoordinates()
        currentSectorCoordinates: Coordinates = self._intelligence.generateSectorCoordinates()

        playerList: SpriteList = SpriteList()
        playerList.append(self._enterprise)

        self._quadrant.placeEnterprise(self._enterprise, currentSectorCoordinates)

        self._quadrantMediator: QuadrantMediator = QuadrantMediator()

        self._quadrantMediator.playerList = playerList
        if self.logger.getEffectiveLevel() == DEBUG:
            self._quadrant.addKlingon()

        if self._quadrant.klingonCount > 0:
            klingonSprites: SpriteList = SpriteList()
            for klingon in self._quadrant._klingons:
                klingonSprites.append(klingon)

            self._quadrantMediator.klingonList = klingonSprites
        else:
            self._quadrantMediator.klingonList = SpriteList()

        self.logger.info(f'Setup Complete')

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        start_render()

        # Call draw() on all your sprite lists below
        # self._backgroundSprite.gridSpriteList.draw()
        # Draw the background texture
        draw_lrwh_rectangle_textured(bottom_left_x=1, bottom_left_y=CONSOLE_HEIGHT,
                                     width=SCREEN_WIDTH, height=QUADRANT_GRID_HEIGHT, texture=self.background)

        self._quadrantMediator.playerList.draw()
        self._quadrantMediator.klingonList.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.physicsEngine.update()
        self._quadrantMediator.update(quadrant=self._quadrant)
        self._quadrantMediator.playerList.update()

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
        elif pressedKey == arcade.key.G:
            from pytrek.gui.GalaxyView import GalaxyView

            galaxyView: GalaxyView = GalaxyView(gameView=self)
            self.window.show_view(galaxyView)

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


def main():
    """ Main method """
    arcadeWindow: Window     = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    gameView:     PyTrekView = PyTrekView()

    arcadeWindow.show_view(gameView)

    gameView.setup()
    arcade.run()


if __name__ == "__main__":
    main()
