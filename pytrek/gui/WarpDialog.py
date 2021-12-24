from logging import Logger
from logging import getLogger
from typing import Dict

from arcade import Texture
from arcade import View
from arcade import Window
from arcade import color
from arcade import load_texture
from arcade import start_render

from arcade.gui import UIAnchorWidget
from arcade.gui import UIBoxLayout
from arcade.gui import UIInputText
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UIOnClickEvent
from arcade.gui import UITextureButton

from pytrek.LocateResources import LocateResources


class WarpDialog(View):

    def __init__(self, window: Window = None):

        super().__init__(window=window)

        self.logger: Logger = getLogger(__name__)

        self._uiManager:     UIManager  = UIManager()

        self._uiManager.enable()

        self.background_color = color.BLUE

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='EmptySpace.png')

        self._inputTexture: Texture = load_texture(fqFileName)

        # Create a vertical BoxGroup to align label text items
        self._vBox: UIBoxLayout = UIBoxLayout(vertical=True)

        warpFactorInputBox: UIBoxLayout = self._createWarpFactorInputBox()
        quadrantInputBox:   UIBoxLayout = self._createInputQuadrant()
        buttonBox:          UIBoxLayout = self._createDialogButtons()

        self._vBox.add(warpFactorInputBox.with_border(width=1, color=color.WHITE).with_space_around(bottom=10))
        self._vBox.add(quadrantInputBox.with_border(width=1, color=color.WHITE).with_space_around(bottom=10))
        self._vBox.add(buttonBox.with_border(width=1, color=color.WHITE))

        self._uiManager.add(
            UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                align_y=10,
                child=self._vBox)
        )

    def on_draw(self):
        start_render()
        self._uiManager.draw()

    def _createWarpFactorInputBox(self) -> UIBoxLayout:

        warpFactorInputBox: UIBoxLayout = UIBoxLayout(width=400, vertical=False, align='x:right, y:center')

        warpLabel: UILabel     = self._createLabel(text='Warp Factor: ')
        warpInput: UIInputText = UIInputText(text='555555', height=18, width=100, font_size=12, text_color=color.BLACK)

        warpFactorInputBox.add(
            warpLabel.with_space_around(left=5, top=5)
        )
        warpFactorInputBox.add(warpInput
                               .with_border(width=2, color=color.WHITE)
                               .with_space_around(left=5, right=5, top=10)
                               .with_background(texture=self._inputTexture)
                               )

        return warpFactorInputBox

    def _createInputQuadrant(self) -> UIBoxLayout:

        quadrantLabel: UILabel = self._createLabel('Quadrant; ')

        quadrantLayout: UIBoxLayout = UIBoxLayout(vertical=False)

        xCoordinate: UIInputText = UIInputText(text='0', height=18, width=100, font_size=12, text_color=color.BLACK)

        quadrantLayout.add(xCoordinate
                           .with_border(width=2, color=color.WHITE)
                           .with_space_around(left=5, top=5)
                           .with_background(texture=self._inputTexture)
                           )

        mainLayout: UIBoxLayout = UIBoxLayout(width=300, vertical=False)

        mainLayout.add(quadrantLabel.with_space_around(left=5, top=5))
        mainLayout.add(quadrantLayout)

        return mainLayout

    def _createDialogButtons(self) -> UIBoxLayout:
        """
        Creates and binds the dialog 'Ok' and 'Cancel' buttons

        Returns:  The button box container
        """
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='OkButton.png')

        okButtonTexture: Texture = load_texture(fqFileName)
        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='OkButtonPressed.png')
        okButtonPressedTexture: Texture = load_texture(fqFileName)

        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='CancelButton.png')

        cancelButtonTexture: Texture = load_texture(fqFileName)

        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='CancelButtonPressed.png')

        cancelButtonPressedTexture: Texture = load_texture(fqFileName)

        buttonBox: UIBoxLayout = UIBoxLayout(width=300, vertical=False)
        buttonStyle: Dict = {'font_name': 'arial',
                             'font_size': 12
                             }
        # okButton: UIFlatButton = UIFlatButton(text='Ok', width=75, height=35, style=buttonStyle)
        okButton: UITextureButton = UITextureButton(width=35, height=35,
                                                    texture=okButtonTexture,
                                                    texture_pressed=okButtonPressedTexture,
                                                    style=buttonStyle)

        # cancelButton: UIFlatButton = UIFlatButton(text='Cancel', width=75, height=35, style=buttonStyle)
        cancelButton: UITextureButton = UITextureButton(width=35, height=35,
                                                        texture=cancelButtonTexture,
                                                        texture_pressed=cancelButtonPressedTexture,
                                                        style=buttonStyle)

        buttonBox.add(okButton.with_space_around(top=10, bottom=10, left=5))
        buttonBox.add(cancelButton.with_space_around(top=10, bottom=10, left=5, right=5))

        okButton.on_click = self._onClickOk
        cancelButton.on_click = self._onClickCancel

        return buttonBox

    def setup(self):
        pass

    def _onClickOk(self, event: UIOnClickEvent):
        print(f'{event.source.text} button pressed')

    def _onClickCancel(self, event: UIOnClickEvent):
        print(f'{event.source.text} button pressed')

    def _createLabel(self, text: str = '') -> UILabel:

        uiLabel: UILabel = UILabel(text=text, height=16, font_size=12, bold=True)

        return uiLabel
