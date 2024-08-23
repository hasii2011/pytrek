
from logging import Logger
from logging import getLogger

from arcade import Section
from arcade import Texture
from arcade import load_texture

from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import SCREEN_WIDTH

from pytrek.GameState import GameState

from pytrek.LocateResources import LocateResources

from pytrek.mediators.GalaxyViewMediator import GalaxyViewMediator


class GalaxySection(Section):
    def __init__(self, left: int, bottom: int, width: int, height: int):

        super().__init__(left, bottom, width, height, modal=True, enabled=False)

        self.logger: Logger = getLogger(__name__)

        fqFileName: str = LocateResources.getImagePath(bareFileName='GalaxyScanBackground.png')

        self._texture: Texture = load_texture(fqFileName)

        self._gameState: GameState          = GameState()
        self._mediator:  GalaxyViewMediator = GalaxyViewMediator()

    def on_draw(self):
        centerX: float = SCREEN_WIDTH / 2
        centerY: float = (QUADRANT_GRID_HEIGHT / 2) + CONSOLE_SECTION_HEIGHT

        self._texture.draw_sized(center_x=centerX, center_y=centerY, width=SCREEN_WIDTH, height=QUADRANT_GRID_HEIGHT)

        self._mediator.draw(centerCoordinates=self._gameState.currentQuadrantCoordinates)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Check if any button is pressed;  Go back to the main game
        """
        self.enabled = False

