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
from arcade.gui import UIFlatButton
from arcade.gui import UIInputText
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UIOnClickEvent

from pytrek.LocateResources import LocateResources


class WarpDialog(View):

    def __init__(self, window: Window = None):

        super().__init__(window=window)

        self.logger: Logger = getLogger(__name__)

        self._uiManager:     UIManager  = UIManager()

        self._uiManager.enable()

        self.background_color = color.BLUE

        # Create a vertical BoxGroup to align label text items
        self._vBox: UIBoxLayout = UIBoxLayout(vertical=True)

        warpFactorInputBox: UIBoxLayout = self._createWarpFactorInputBox()
        buttonBox:          UIBoxLayout = self._createDialogButtons()

        self._vBox.add(warpFactorInputBox.with_border(width=1, color=color.WHITE).with_space_around(bottom=10))
        self._vBox.add(buttonBox.with_border(width=1, color=color.WHITE))

        self._uiManager.add(
            UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                align_y=10,
                child=self._vBox)
        )

    def _createWarpFactorInputBox(self) -> UIBoxLayout:

        warpFactorInputBox: UIBoxLayout = UIBoxLayout(width=400, vertical=False, align='x:right, y:center')

        warpLabel: UILabel     = UILabel(text='Warp Factor: ', height=16, font_size=12, bold=True)
        warpInput: UIInputText = UIInputText(width=100, height=16, font_size=12, text_color=color.WHITE, text='555555')

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='EmptySpace.png')

        texture: Texture = load_texture(fqFileName)

        warpFactorInputBox.add(
            warpLabel.with_space_around(left=5, top=5)
        )
        warpFactorInputBox.add(
            warpInput.with_border(width=2, color=color.WHITE).with_space_around(left=5, right=5, top=10).with_background(texture=texture)
        )

        return warpFactorInputBox

    def _createDialogButtons(self) -> UIBoxLayout:
        """
        Creates and binds the dialog 'Ok' and 'Cancel' buttons

        Returns:  The button box container
        """

        buttonBox: UIBoxLayout = UIBoxLayout(width=300, vertical=False)
        buttonStyle: Dict = {'font_name': 'arial',
                             'font_size': 12
                             }
        okButton: UIFlatButton = UIFlatButton(text='Ok', width=75, height=35, style=buttonStyle)
        cancelButton: UIFlatButton = UIFlatButton(text='Cancel', width=75, height=35, style=buttonStyle)
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

    def on_draw(self):
        start_render()
        self._uiManager.draw()
