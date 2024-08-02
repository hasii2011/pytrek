
from logging import Logger
from logging import getLogger

from arcade import Texture
from arcade import View
from arcade import Window
from arcade import draw_lrwh_rectangle_textured
from arcade import load_texture

from arcade import run as arcadeRun
from arcade import start_render

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import QUADRANT_GRID_WIDTH
from pytrek.Constants import SCREEN_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.Constants import STATUS_VIEW_WIDTH
from pytrek.GameState import GameState

from pytrek.LocateResources import LocateResources
from pytrek.PyTrekView import SCREEN_TITLE
from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.guiv2.StatusConsoleSection import StatusConsoleSection
from pytrek.mediators.QuadrantMediator import QuadrantMediator
from pytrek.model.Galaxy import Galaxy
from pytrek.settings.GameSettings import GameSettings


class PyTrekV2(View):

    def __init__(self):

        LocateResources.setupSystemLogging()

        self.logger: Logger = getLogger(__name__)
        super().__init__()

        fqFileName:      str     = LocateResources.getImagePath(bareFileName='QuadrantBackground.png')
        self.background: Texture = load_texture(fqFileName)

        self._gameSettings: GameSettings = GameSettings()     # Be able to read the preferences file
        self._gameState:    GameState    = GameState()        # Set up the game parameters which uses the above
        self._gameEngine:   GameEngine   = GameEngine()       # Then the engine needs to be initialized
        self._intelligence: Intelligence = Intelligence()
        self._computer:     Computer     = Computer()
        self._galaxy:       Galaxy       = Galaxy()           # This essentially finishes initializing most of the game

        self._quadrantMediator: QuadrantMediator   = QuadrantMediator()

        self._quadrant           = self._galaxy.currentQuadrant

        left:   int = QUADRANT_GRID_WIDTH
        bottom: int = QUADRANT_GRID_HEIGHT
        height: int = QUADRANT_GRID_HEIGHT + CONSOLE_HEIGHT
        width:  int = STATUS_VIEW_WIDTH
        self._statusConsole: StatusConsoleSection = StatusConsoleSection(left=left, bottom=bottom, height=height, width=width)

        # add the sections
        self.section_manager.add_section(self._statusConsole)

        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates

        self._enterprise: Enterprise = self._gameState.enterprise

        # And finally the rest of the UI elements
        self._quadrantMediator.enterQuadrant(quadrant=self._quadrant, enterprise=self._enterprise)

    def on_draw(self):
        start_render()
        # Draw the background texture
        draw_lrwh_rectangle_textured(bottom_left_x=1, bottom_left_y=CONSOLE_HEIGHT,
                                     width=SCREEN_WIDTH, height=QUADRANT_GRID_HEIGHT, texture=self.background)



def main():
    arcadeWindow: Window   = Window(title=SCREEN_TITLE, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    game:         PyTrekV2 = PyTrekV2()

    arcadeWindow.show_view(game)

    arcadeRun()


if __name__ == '__main__':
    main()
