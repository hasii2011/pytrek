
from typing import Callable
from typing import Dict
from typing import cast

from dataclasses import dataclass

from enum import Enum

from logging import Logger
from logging import getLogger

from arcade import Texture
from arcade import View
from arcade import Window
from arcade import color

from arcade.gui import UIAnchorWidget
from arcade.gui import UIBoxLayout
from arcade.gui import UIInputText
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UIOnClickEvent
from arcade.gui import UITextureButton

from arcade import load_texture
from arcade import start_render

from pytrek.gui.StdMsgBox import StdMsgBox
from pytrek.model.Coordinates import Coordinates

from pytrek.LocateResources import LocateResources


class DialogAnswer(Enum):
    Cancelled = 'Cancelled'
    Ok = 'Ok'


@dataclass
class WarpTravelAnswer:
    """
    The `course` and `distance` values are only valid when dialogAnswer is DialogAnswer.Ok
    """
    dialogAnswer: DialogAnswer = DialogAnswer.Cancelled

    coordinates: Coordinates = Coordinates(x=-1, y=-1)
    warpFactor:  float = 0.0


# TODO:  Figure how to tell callable function returns nothing and make mypy happy
# DialogCallback = NewType('DialogCallback', Callable[[WarpTravelAnswer], None])  # type: ignore
DialogCallback = Callable[[WarpTravelAnswer], None]


class WarpDialog(View):
    """

    """
    WARP_FACTOR_ERROR_MESSAGE: str = 'Warp Factor must be a float between 1.0 and 9.9'
    COORDINATES_ERROR_MESSAGE: str = 'Quadrant coordinates must be integers between 0 and 9'

    def __init__(self, window: Window, completeCallback: DialogCallback):

        super().__init__(window=window)

        self._callback:  DialogCallback  = completeCallback
        self.logger:     Logger          = getLogger(__name__)
        self._uiManager: UIManager       = UIManager()

        self._uiManager.enable()

        self.background_color = color.BLUE

        self._warpFactorInput:  UIInputText = cast(UIInputText, None)
        self._xCoordinateInput: UIInputText = cast(UIInputText, None)
        self._yCoordinateInput: UIInputText = cast(UIInputText, None)

        fqFileName: str = LocateResources.getImagePath(bareFileName='EmptySpace.png')

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

        # warpFactorInputBox: UIBoxLayout = UIBoxLayout(width=400, vertical=False, align='x:right, y:center')
        warpFactorInputBox: UIBoxLayout = UIBoxLayout(vertical=False, align='x:right, y:center')

        warpLabel: UILabel     = self._createLabel(text='Warp Factor: ')
        warpInput: UIInputText = UIInputText(text='5', height=18, width=100, font_size=12, text_color=color.BLACK)

        warpFactorInputBox.add(
            warpLabel.with_space_around(left=5, top=5)
        )
        warpFactorInputBox.add(warpInput
                               .with_border(width=2, color=color.WHITE)
                               .with_space_around(left=5, right=5, top=10)
                               .with_background(texture=self._inputTexture)
                               )

        self._warpFactorInput = warpInput
        return warpFactorInputBox

    def _createInputQuadrant(self) -> UIBoxLayout:

        quadrantLabel: UILabel = self._createLabel('Quadrant; ')

        quadrantLayout: UIBoxLayout = UIBoxLayout(vertical=False)

        xCoordinate: UIInputText = UIInputText(text='0', height=18, width=50, font_size=12, text_color=color.BLACK)
        yCoordinate: UIInputText = UIInputText(text='0', height=18, width=50, font_size=12, text_color=color.BLACK)

        quadrantLayout.add(xCoordinate
                           .with_border(width=2, color=color.WHITE)
                           .with_space_around(left=5, right=5, top=10)
                           .with_background(texture=self._inputTexture)
                           )

        quadrantLayout.add(yCoordinate
                           .with_border(width=2, color=color.WHITE)
                           .with_space_around(left=5, right=5, top=10)
                           .with_background(texture=self._inputTexture)
                           )

        # mainLayout: UIBoxLayout = UIBoxLayout(width=300, vertical=False)
        mainLayout: UIBoxLayout = UIBoxLayout(vertical=False)

        mainLayout.add(quadrantLabel.with_space_around(left=47, top=5))
        mainLayout.add(quadrantLayout)

        self._xCoordinateInput = xCoordinate
        self._yCoordinateInput = yCoordinate

        return mainLayout

    def _createDialogButtons(self) -> UIBoxLayout:
        """
        Creates and binds the dialog 'Ok' and 'Cancel' buttons

        Returns:  The button box container
        """
        fqFileName: str = LocateResources.getImagePath(bareFileName='OkButton.png')

        okButtonTexture: Texture = load_texture(fqFileName)
        fqFileName = LocateResources.getImagePath(bareFileName='OkButtonPressed.png')
        okButtonPressedTexture: Texture = load_texture(fqFileName)

        fqFileName = LocateResources.getImagePath(bareFileName='CancelButton.png')

        cancelButtonTexture: Texture = load_texture(fqFileName)

        fqFileName = LocateResources.getImagePath(bareFileName='CancelButtonPressed.png')

        cancelButtonPressedTexture: Texture = load_texture(fqFileName)

        # buttonBox: UIBoxLayout = UIBoxLayout(width=300, vertical=False)
        buttonBox: UIBoxLayout = UIBoxLayout(vertical=False)
        buttonStyle: Dict = {'font_name': 'arial',
                             'font_size': 12
                             }
        okButton: UITextureButton = UITextureButton(width=35, height=35,
                                                    texture=okButtonTexture,
                                                    texture_pressed=okButtonPressedTexture,
                                                    style=buttonStyle)

        cancelButton: UITextureButton = UITextureButton(width=35, height=35,
                                                        texture=cancelButtonTexture,
                                                        texture_pressed=cancelButtonPressedTexture,
                                                        style=buttonStyle)

        buttonBox.add(okButton.with_space_around(top=10, bottom=10, left=5))
        buttonBox.add(cancelButton.with_space_around(top=10, bottom=10, left=5, right=5))

        @okButton.event('on_click')
        def onClickOk(event: UIOnClickEvent):
            self._onClickOk(event)

        @cancelButton.event('on_click')
        def onClickCancel(event: UIOnClickEvent):
            self._onClickCancel(event)

        return buttonBox

    def setup(self):
        pass

    # noinspection PyUnusedLocal
    def _onClickOk(self, event: UIOnClickEvent):

        warpFactor:  str = self._warpFactorInput.text
        xCoordinate: str = self._xCoordinateInput.text
        yCoordinate: str = self._yCoordinateInput.text

        if self.__validateDialogInputs(warpFactor=warpFactor, xCoordinate=xCoordinate, yCoordinate=yCoordinate) is True:

            warpTravelAnswer: WarpTravelAnswer = WarpTravelAnswer()

            warpTravelAnswer.dialogAnswer = DialogAnswer.Ok
            warpTravelAnswer.warpFactor   = float(warpFactor)
            warpTravelAnswer.coordinates  = Coordinates(x=int(xCoordinate), y=int(yCoordinate))

            self._callback(warpTravelAnswer)

    # noinspection PyUnusedLocal
    def _onClickCancel(self, event: UIOnClickEvent):

        warpTravelAnswer: WarpTravelAnswer = WarpTravelAnswer()

        self._callback(warpTravelAnswer)

    def _createLabel(self, text: str = '') -> UILabel:

        uiLabel: UILabel = UILabel(text=text, font_name='Kenney Future', height=16, font_size=12, bold=True)

        return uiLabel

    def __validateDialogInputs(self, warpFactor: str, xCoordinate: str, yCoordinate: str) -> bool:

        valid: bool = self.__validateWarpFactor(warpFactor)
        if valid is True:
            valid = self.__validateCoordinate(coordinate=xCoordinate)
            if valid is True:
                valid = self.__validateCoordinate(coordinate=yCoordinate)

        return valid

    def __validateWarpFactor(self, warpFactor: str) -> bool:
        valid: bool = True

        try:
            floatWarp: float = float(warpFactor)
            if floatWarp < 0 or floatWarp > 9.9:
                self._displayError(WarpDialog.WARP_FACTOR_ERROR_MESSAGE)
        except ValueError as e:
            self._displayError(WarpDialog.WARP_FACTOR_ERROR_MESSAGE)
            self.logger.error(f'{e}')
            valid = False

        return valid

    def __validateCoordinate(self, coordinate: str):
        valid: bool = True

        try:
            intCoordinate: int = int(coordinate)
            if intCoordinate < 0 or intCoordinate > 9:
                self._displayError(WarpDialog.COORDINATES_ERROR_MESSAGE)

        except ValueError as e:
            self._displayError(WarpDialog.COORDINATES_ERROR_MESSAGE)
            self.logger.error(f'{e}')
            valid = False

        return valid

    def _displayError(self, msg: str):

        StdMsgBox.displayMessageBox(uiManager=self._uiManager, msg=msg)
