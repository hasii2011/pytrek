
from logging import Logger
from logging import getLogger

from arcade import Texture
from arcade import View
from arcade import Window
from arcade import color
from arcade import load_texture
from arcade.gui import UIAnchorWidget
from arcade.gui import UIBoxLayout
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UIPadding
from arcade.gui import UITextArea

from arcade import start_render

from arcade import key as arcadeKey
from arcade.gui import UITextureButton
from arcade.gui import UITexturePane

from pytrek.LocateResources import LocateResources


class HelpView(View):

    FONT_NAME: str = 'UniverseCondensed'

    def __init__(self, window: Window):

        super().__init__(window=window)

        self.logger: Logger = getLogger(__name__)

        self._uiManager: UIManager = UIManager()

        self._uiManager.enable()

        window.background_color = color.BLUE_YONDER

        title:               UILabel        = self._createLabel(text='PyArcadeStarTrek Help', height=24, fontSize=18)
        wrappedHelpTextArea: UITexturePane  = self._createHelpTextArea()

        padding:   UIPadding = UIPadding(child=wrappedHelpTextArea, padding=(4, 4, 4, 4))
        buttonBox: UIBoxLayout = self._createScrollButtonContainer()

        hBox: UIBoxLayout = UIBoxLayout(vertical=False,
                                        children=[
                                            padding.with_border(width=2, color=color.WHITE).with_space_around(bottom=10, top=10),
                                            buttonBox.with_space_around(left=15, top=20),
                                        ])

        mainBox: UIBoxLayout = UIBoxLayout(vertical=True,
                                           children=[
                                               title.with_space_around(top=20),
                                               hBox
                                           ])

        self._uiManager.add(
            UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="top",
                child=mainBox)
        )

    def on_draw(self):
        """
        Draw this view
        """
        start_render()
        self._uiManager.draw()

    def on_key_release(self, releasedKey: int, key_modifiers: int):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if releasedKey == arcadeKey.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)

    def _createLabel(self, text: str = '', height: int = 16, fontSize: int = 12) -> UILabel:

        uiLabel: UILabel = UILabel(text=text, font_name=HelpView.FONT_NAME, height=height, font_size=fontSize, bold=True)
        return uiLabel

    def _createScrollButtonContainer(self) -> UIBoxLayout:

        upButton:   UITextureButton = self._createTextureButton(bareFileName='ArrowUp')
        downButton: UITextureButton = self._createTextureButton(bareFileName='ArrowDown')

        buttonBox: UIBoxLayout = UIBoxLayout(vertical=True,
                                             children=[
                                                 upButton.with_space_around(top=20),
                                                 downButton.with_space_around(bottom=10, top=10)
                                             ])

        return buttonBox

    def _createHelpTextArea(self) -> UITexturePane:
        """
        Creates and loads the help text

        Returns:  The UITextArea loaded with help text wrapped by
        a nice texture pane
        """
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.RESOURCES_PACKAGE_NAME,
                                                           bareFileName='Help.txt')
        with open(fqFileName) as fd:
            lines: str = fd.read()
        textArea: UITextArea = UITextArea(width=550, height=360,
                                          text=lines,
                                          text_color=color.BLACK,
                                          font_name=HelpView.FONT_NAME)

        textureFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                                bareFileName='GreyPanel.png')
        background: Texture = load_texture(textureFileName)

        texturePane: UITexturePane = UITexturePane(
            textArea.with_space_around(right=20),
            tex=background,
            padding=(10, 10, 10, 10)
        )

        return texturePane

    def _createTextureButton(self, bareFileName: str) -> UITextureButton:

        normalFileName:  str = f'{bareFileName}.png'
        pressedFileName: str = f'{bareFileName}Pressed.png'
        hoveredFileName: str = f'{bareFileName}Hovered.png'

        fqNormalFileName:  str = LocateResources.getResourcesPath(LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=normalFileName)
        fqPressedFileName: str = LocateResources.getResourcesPath(LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=pressedFileName)
        fqHoveredFileName: str = LocateResources.getResourcesPath(LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=hoveredFileName)

        normalTexture:  Texture = load_texture(fqNormalFileName)
        pressedTexture: Texture = load_texture(fqPressedFileName)
        hoveredTexture: Texture = load_texture(fqHoveredFileName)

        button: UITextureButton = UITextureButton(texture=normalTexture,
                                                  texture_pressed=pressedTexture,
                                                  texture_hovered=hoveredTexture,
                                                  width=32, height=32)

        return button
