
from logging import Logger
from logging import getLogger

from arcade import Rect
from arcade import Section
from arcade import Texture
from arcade import draw_texture_rect
from arcade import load_texture

from pytrek.Constants import CONSOLE_SECTION_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import SCREEN_WIDTH

from pytrek.GameState import GameState

from pytrek.LocateResources import LocateResources

from pytrek.mediators.GalaxyViewMediator import GalaxyViewMediator


class GalaxySection(Section):
    """
    Represents a full-screen overlay view of the Galaxy (typically shown when performing a "Galaxy Chart" scan).

    Functionality:
    1. State & Display Overlay:
       - Initialized as a modal section (modal=True) that starts disabled (enabled=False).
       - Renders a custom background texture loaded from GalaxyScanBackground.png centered on the quadrant grid area.
       - Leverages a GalaxyViewMediator to draw the layout of the galaxy's quadrants, highlighting the Captain's
         current position (self._gameState.currentQuadrantCoordinates).
    2. User Interaction:
       - Responds to any mouse click (on_mouse_press) by setting self.enabled = False. This immediately closes/dismisses
       the overlay and returns the user to the active quadrant view of the game.
    """
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

        rect: Rect = Rect.from_kwargs(x=centerX, y=centerY, width=SCREEN_WIDTH, height=QUADRANT_GRID_HEIGHT)
        draw_texture_rect(self._texture, rect)
        self._mediator.draw(centerCoordinates=self._gameState.currentQuadrantCoordinates)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Check if any button is pressed;  Go back to the main game
        """
        self.enabled = False
