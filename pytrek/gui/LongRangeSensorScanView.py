
from arcade import View
from arcade import load_texture
from arcade import start_render

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import SCREEN_WIDTH
from pytrek.GameState import GameState

from pytrek.LocateResources import LocateResources

from pytrek.PyTrek import PyTrekView

from pytrek.engine.GameEngine import GameEngine

from pytrek.mediators.LongRangeSensorScanMediator import LongRangeSensorScanMediator

from pytrek.model.Coordinates import Coordinates


class LongRangeSensorScanView(View):
    """
    Displays a long range sensor scan.  Essentially, only the quadrant adjacent to the on the Enterprise is in
    """
    BACKGROUND_WIDTH: int  = 321
    BACKGROUND_HEIGHT: int = 322

    def __init__(self, gameView: PyTrekView):

        super().__init__()

        self._gameView: PyTrekView = gameView
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='LongRangeSensorBackground.png')

        self.texture = load_texture(fqFileName)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        # set_viewport(0, QUADRANT_GRID_WIDTH - 1, 0, QUADRANT_GRID_HEIGHT - 1)

        self._lrScanViewMediator: LongRangeSensorScanMediator = LongRangeSensorScanMediator()
        self._gameEngine:         GameEngine                  = GameEngine()
        self._gameState:          GameState                   = GameState()

    def on_draw(self):
        """
        Draw this view
        """
        start_render()
        centerX: float = SCREEN_WIDTH / 2
        centerY: float = (QUADRANT_GRID_HEIGHT / 2) + CONSOLE_HEIGHT

        self.texture.draw_sized(center_x=centerX, center_y=centerY, width=321, height=322)

        coordinates: Coordinates = self._gameState.currentQuadrantCoordinates
        self._lrScanViewMediator.update(coordinates)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        If the user presses the mouse button, go back to the game
        """
        self.window.show_view(self._gameView)
