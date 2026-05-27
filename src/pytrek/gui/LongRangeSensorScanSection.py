
from logging import Logger
from logging import getLogger

from arcade import Rect
from arcade import Section
from arcade import Texture
from arcade import load_texture
from arcade import draw_texture_rect

from pytrek.Constants import SCREEN_WIDTH
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import CONSOLE_SECTION_HEIGHT

from pytrek.GameState import GameState

from pytrek.LocateResources import LocateResources

from pytrek.engine.GameEngine import GameEngine

from pytrek.mediators.LongRangeSensorScanMediator import LongRangeSensorScanMediator

from pytrek.model.Coordinates import Coordinates


class LongRangeSensorScanSection(Section):
    """
    The LongRangeSensorScanSection class displays a pop-up overlay scan containing sensor data for the quadrants
    immediately adjacent to the Enterprise's current position.

    Functionality:

    1. State & Overlay Setup:
    - Initialized as a modal section (`modal=True`) that starts disabled (`enabled=False`).
    - Renders a custom overlay background loaded from `LongRangeSensorBackground.png` centered horizontally and vertically on the quadrant grid area.

    2. Long-Range Data Rendering:
    - Delegates scan drawing to the LongRangeSensorScanMediator.
    - Passes the current quadrant coordinates (`self._gameState.currentQuadrantCoordinates`)
    to the mediator during `on_draw` to populate adjacent quadrant details.

    3. User Interaction:
    - Listens to any mouse click (`on_mouse_press`) to set `self.enabled = False`, which
    immediately closes/dismisses the overlay scanner and returns the user to the active quadrant view.
    """

    BACKGROUND_WIDTH: int  = 321
    BACKGROUND_HEIGHT: int = 322

    def __init__(self, left: int, bottom: int, width: int, height: int):

        super().__init__(left, bottom, width, height, modal=True, enabled=False)

        self.logger: Logger = getLogger(__name__)

        fqFileName: str = LocateResources.getImagePath(bareFileName='LongRangeSensorBackground.png')

        self._texture: Texture = load_texture(fqFileName)

        self._graphicCenterX: float = SCREEN_WIDTH / 2
        self._graphicCenterY: float = (QUADRANT_GRID_HEIGHT / 2) + CONSOLE_SECTION_HEIGHT

        self._mediator: LongRangeSensorScanMediator = LongRangeSensorScanMediator(view=self,
                                                                                  graphicCenterX=self._graphicCenterX,
                                                                                  graphicCenterY=self._graphicCenterY)

        self._gameEngine: GameEngine = GameEngine()
        self._gameState:  GameState  = GameState()

    def on_draw(self):
        """
        Draw this view with the help of the mediator.  We only draw the graphics;
        The mediator interacts with the game engine and the game state which are non-graphical
        elements
        """

        # self._texture.draw_sized(center_x=self._graphicCenterX,
        #                          center_y=self._graphicCenterY,
        #                          width=LongRangeSensorScanSection.BACKGROUND_WIDTH,
        #                          height=LongRangeSensorScanSection.BACKGROUND_HEIGHT)

        rect: Rect = Rect.from_kwargs(x=self._graphicCenterX,
                                      y=self._graphicCenterY,
                                      width=LongRangeSensorScanSection.BACKGROUND_WIDTH,
                                      height=LongRangeSensorScanSection.BACKGROUND_HEIGHT
                                      )
        draw_texture_rect(self._texture, rect)

        coordinates: Coordinates = self._gameState.currentQuadrantCoordinates
        self._mediator.draw(coordinates)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Check if any button is pressed;  Go back to the main game
        """
        self.enabled = False
