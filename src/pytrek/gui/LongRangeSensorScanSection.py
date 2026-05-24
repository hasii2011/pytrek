
from logging import Logger
from logging import getLogger

from arcade import Rect
from arcade import Section
from arcade import Texture
from arcade import load_texture
from arcade import draw_texture_rect

from src.pytrek.Constants import SCREEN_WIDTH
from src.pytrek.Constants import QUADRANT_GRID_HEIGHT
from src.pytrek.Constants import CONSOLE_SECTION_HEIGHT

from src.pytrek.GameState import GameState

from src.pytrek.LocateResources import LocateResources

from src.pytrek.engine.GameEngine import GameEngine

from src.pytrek.mediators.LongRangeSensorScanMediator import LongRangeSensorScanMediator

from src.pytrek.model.Coordinates import Coordinates


class LongRangeSensorScanSection(Section):
    """
    Displays a long range sensor scan.  Essentially, only the quadrant adjacent to the on the Enterprise is in
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
