from arcade import start_render

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import QUADRANT_GRID_HEIGHT
from pytrek.Constants import SCREEN_WIDTH

from arcade import View
from arcade import load_texture

from pytrek.LocateResources import LocateResources

from pytrek.PyTrek import PyTrekView


class GalaxyView(View):

    def __init__(self, gameView: PyTrekView):

        super().__init__()

        self._gameView: PyTrekView = gameView
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='GalaxyScanBackground.png')

        self.texture = load_texture(fqFileName)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        # set_viewport(0, QUADRANT_GRID_WIDTH - 1, 0, QUADRANT_GRID_HEIGHT - 1)

    def on_draw(self):
        """
        Draw this view
        """
        start_render()
        centerX: float = SCREEN_WIDTH / 2
        centerY: float = (QUADRANT_GRID_HEIGHT / 2) + CONSOLE_HEIGHT

        self.texture.draw_sized(center_x=centerX, center_y=centerY,
                                width=SCREEN_WIDTH, height=QUADRANT_GRID_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        If the user presses the mouse button, re-start the game.
        """
        self.window.show_view(self._gameView)
