
from typing import Callable
from typing import NewType
from typing import Optional
from typing import cast

from enum import Enum

from dataclasses import dataclass

from logging import Logger
from logging import getLogger

from arcade import View
from arcade import color
from arcade import draw_lrwh_rectangle_textured
# from arcade import key
from arcade import load_texture
from arcade import start_render

from arcade.gui import UIFlatButton
from arcade.gui import UIInputBox
from arcade.gui import UILabel
from arcade.gui import UIManager

from arcade.gui.ui_style import UIStyle

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import MINIMUM_COORDINATE
from pytrek.Constants import MAXIMUM_COORDINATE
from pytrek.Constants import MAXIMUM_WARP_FACTOR_VALUE
from pytrek.Constants import MINIMUM_WARP_FACTOR_VALUE
from pytrek.Constants import QUADRANT_GRID_HEIGHT

from pytrek.LocateResources import LocateResources
from pytrek.model.Coordinates import Coordinates

from tests.TestSpriteSheet import SCREEN_WIDTH


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
DialogCallback = NewType('DialogCallback', Callable[[WarpTravelAnswer], None])  # type: ignore
# DialogCallback = Callable[[WarpTravelAnswer], None]


class DialogButton(UIFlatButton):
    ID_OK:     str = '6666'
    ID_CANCEL: str = '7976'

    def __init__(self, text: str,
                 center_x: int = 0, center_y: int = 0, width:  int = 0,   height: int = 0, align:  str = "center", buttonId: Optional[str] = None,
                 style: UIStyle = None,
                 callback: Callable = cast(Callable, None),
                 **kwargs):

        super().__init__(text=text, center_x=center_x, center_y=center_y, width=width, height=height, align=align, id=buttonId, style=style, **kwargs)

        self._callback: Callable = callback

    def on_click(self):
        """
        Called when user releases button
        To capture a button click, subclass the button and override on_click.
        """
        assert self._callback is not None, 'Developer forgot to associate callback for button'
        self._callback()


FONT_SIZE:              int = 12
LABEL_WIDTH:            int = 125
COORDINATE_INPUT_WIDTH: int = 50
WARP_INPUT_WIDTH:       int = 50
FONT_COLOR = color.BLACK
BG_COLOR   = color.WHITE


class WarpTravelDialog(View):
    """
    Presents a 'pseudo' dialog like UI in order to gather a course and distance value for manual warp
    travel;  Does validation on input and only proceeds if valid input is presented or the player
    cancels the interaction
    """
    INVALID_COORDINATE_MESSAGE:   str = 'Invalid Coordinate (0-9)'
    INVALID_WARP_FACTOR__MESSAGE: str = 'Invalid Warp Factor (1.0 - 9.99)'

    LEN_INVALID_COORDINATE_MESSAGE:  int = len(INVALID_COORDINATE_MESSAGE)
    LEN_INVALID_WARP_FACTOR_MESSAGE: int = len(INVALID_WARP_FACTOR__MESSAGE)

    def __init__(self, completeCallback: DialogCallback):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._completeCallback: DialogCallback = completeCallback

        self._uiManager:     UIManager  = UIManager()

        self._xCoordinateInput: UIInputBox = cast(UIInputBox, None)
        self._yCoordinateInput: UIInputBox = cast(UIInputBox, None)
        self._warpFactorInput:  UIInputBox = cast(UIInputBox, None)
        self._errorLabel:       UILabel    = cast(UILabel, None)

        self._xCoordinate: str  = ''
        self._yCoordinate: str  = ''
        self._warpFactor:  str  = ''

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='QuadrantBackground.png')
        self._background = load_texture(fqFileName)
        self.window.background_color = color.WHITE

    def setup(self):
        """
        Set up pseudo dialog here
        """
        self._uiManager.purge_ui_elements()

        labelX: int = 60
        ySlot:  int = self.window.height // 20

        self._createWarpControls(labelX, ySlot)
        self._createQuadrantControls(labelX, ySlot)

        self._createDialogButtons(ySlot=ySlot)
        self._createErrorLabel(ySlot=ySlot)

    def on_show_view(self):
        """
        Called once when view is activated.
        """
        self.setup()
        # set_background_color(color.WHITE)

    def on_draw(self):
        """
        Draw this view. GUI elements are automatically drawn.
        """
        start_render()
        # Draw the background texture
        draw_lrwh_rectangle_textured(bottom_left_x=1, bottom_left_y=CONSOLE_HEIGHT, width=SCREEN_WIDTH, height=QUADRANT_GRID_HEIGHT, texture=self._background)

    def _createQuadrantControls(self, labelX: int, ySlot: int):
        """
        Creates the x and y coordinate input boxes

        Args:
            labelX:     x point of label
            ySlot:      The y slot position
        """
        inputX: float = labelX * 2 + (COORDINATE_INPUT_WIDTH // 2)    # This works
        inputY: float = ySlot * 3

        quadrantLabel: UILabel     = self._createLabel(text='Quadrant:', centerX=labelX, centerY=inputY, width=LABEL_WIDTH)

        xInput: UIInputBox = UIInputBox(center_x=inputX,                               center_y=inputY, width=COORDINATE_INPUT_WIDTH)
        yInput: UIInputBox = UIInputBox(center_x=inputX + COORDINATE_INPUT_WIDTH + 20, center_y=inputY, width=COORDINATE_INPUT_WIDTH)

        self._setInputStyle(xInput)
        self._setInputStyle(yInput)

        self._uiManager.add_ui_element(quadrantLabel)
        self._uiManager.add_ui_element(xInput)
        self._uiManager.add_ui_element(yInput)

        self._xCoordinateInput = xInput
        self._yCoordinateInput = yInput

    def _createWarpControls(self, labelX: int, ySlot: int):
        """
        Creates the warp factor input box
        Args:
            labelX:     x point of label
            ySlot:      The y slot position
        """

        inputX: float = labelX * 2 + (WARP_INPUT_WIDTH // 2)
        inputY: float = ySlot * 4

        warpFactorLabel: UILabel    = self._createLabel(text='Warp Factor:', centerX=labelX, centerY=inputY, width=LABEL_WIDTH)
        warpFactorInput: UIInputBox = UIInputBox(center_x=inputX, center_y=inputY, width=WARP_INPUT_WIDTH)
        self._setInputStyle(warpFactorInput)

        self._uiManager.add_ui_element(warpFactorLabel)
        self._uiManager.add_ui_element(warpFactorInput)

        self._warpFactorInput = warpFactorInput

    def _createDialogButtons(self, ySlot: int):

        okColumnX:     int = 3 * self.window.width // 14
        cancelColumnX: int = 5 * self.window.width // 14
        centerY:       int = ySlot * 2

        okButton: DialogButton = DialogButton('Ok', callback=self._onOk, buttonId=DialogButton.ID_OK, center_x=okColumnX, center_y=centerY, width=80)
        self._setButtonStyle(dlgButton=okButton)

        cancelButton: DialogButton = DialogButton('Cancel', callback=self._onCancel, buttonId=DialogButton.ID_CANCEL,
                                                  center_x=cancelColumnX, center_y=centerY, width=80)

        self._setButtonStyle(dlgButton=cancelButton)

        self._uiManager.add_ui_element(okButton)
        self._uiManager.add_ui_element(cancelButton)

    def _createErrorLabel(self, ySlot: int):

        width:   int = 480
        centerX: int = width // 2
        centerY: int = ySlot * 1
        self._errorLabel = self._createLabel(text='', centerX=centerX, centerY=centerY, width=width)

        self._uiManager.add_ui_element(self._errorLabel)

    def _createLabel(self, text: str, centerX: float, centerY: float, width: int) -> UILabel:

        label: UILabel = UILabel(text=text, center_x=centerX, center_y=centerY, width=width)
        self._setLabelStyle(label)

        return label

    def _setInputStyle(self, inputBox: UIInputBox):

        inputBox.set_style_attrs(
            font_size=FONT_SIZE,
            font_color=color.WHITE,
            font_color_hover=color.WHITE,
            font_color_focus=color.WHITE,
            bg_color=color.BLACK,
            bg_color_hover=color.BLACK,
            bg_color_press=color.BLACK,
            bg_color_focus=color.BLACK,
            border_color=color.GRAY,
            border_width=2
        )

    def _setLabelStyle(self, label: UILabel):
        label.set_style_attrs(
            font_size=FONT_SIZE,
            font_color=color.BLACK,
            font_color_hover=color.BLACK,
            font_color_press=color.BLACK
        )

    def _setButtonStyle(self, dlgButton: DialogButton):

        dlgButton.set_style_attrs(
            font_size=FONT_SIZE,
            bg_color_press=color.GRAY
        )

    def _onOk(self):

        self._xCoordinate = self._xCoordinateInput.text
        self._yCoordinate = self._yCoordinateInput.text
        self._warpFactor  = self._warpFactorInput.text

        valid: bool = self._validateWarpFactor(self._warpFactor)
        if valid is True:
            valid = self._validateCoordinates(xCoordinate=self._xCoordinate, yCoordinate=self._yCoordinate)
            if valid is True:
                coordinates: Coordinates      = Coordinates(x=int(self._xCoordinate), y=int(self._yCoordinate))
                warpFactor:  float            = float(self._warpFactor)
                answer:      WarpTravelAnswer = WarpTravelAnswer(coordinates=coordinates, warpFactor=warpFactor, dialogAnswer=DialogAnswer.Ok)
                self._errorLabel.text = ''
                self._uiManager.purge_ui_elements()
                self._completeCallback(answer)
            else:
                self._errorLabel.text = WarpTravelDialog.INVALID_COORDINATE_MESSAGE
        else:
            self._errorLabel.text = WarpTravelDialog.INVALID_WARP_FACTOR__MESSAGE

        self.logger.info(f"{self._xCoordinate=} {self._yCoordinate=} {self._warpFactor=}")

    def _onCancel(self):

        answer: WarpTravelAnswer = WarpTravelAnswer(coordinates=Coordinates(-1, -1), warpFactor=0.0, dialogAnswer=DialogAnswer.Cancelled)

        self._uiManager.purge_ui_elements()
        self._completeCallback(answer)

    def _validateCoordinates(self, xCoordinate: str, yCoordinate: str) -> bool:

        xValid: bool = self._validateIntegerValue(value=xCoordinate, low=MINIMUM_COORDINATE, high=MAXIMUM_COORDINATE, errorLogMsg='Invalid X Coordinate: ')
        yValid: bool = self._validateIntegerValue(value=yCoordinate, low=MINIMUM_COORDINATE, high=MAXIMUM_COORDINATE, errorLogMsg='Invalid Y Coordinate: ')

        if xValid is True and yValid is True:
            return True
        else:
            return False

    def _validateWarpFactor(self, warpFactor: str) -> bool:
        return self._validateFloatValue(value=warpFactor, low=MINIMUM_WARP_FACTOR_VALUE, high=MAXIMUM_WARP_FACTOR_VALUE, errorLogMsg='Warp Factor Input error:')

    def _validateIntegerValue(self, value: str, low: int, high: int, errorLogMsg: str) -> bool:
        """
        Validates both that the string can be an integer and that it falls within the
        bounds

        Args:
            value:   The string value
            low:     The smallest value it can be
            high:    The largest value it can be
            errorLogMsg: The message to log on validation failure

        Returns:  `True` if good else `False`
        """
        try:
            intValue: int = int(value)
            return self._isValidValue(value=intValue, low=low, high=high)
        except ValueError as ve:
            self.logger.error(f'{errorLogMsg}: {ve}')
            return False

    def _validateFloatValue(self, value: str, low: float, high: float, errorLogMsg: str) -> bool:
        """
        Validates both that the string can be an integer and that it falls within the
        bounds

        Args:
            value:   The string value
            low:     The smallest value it can be
            high:    The largest value it can be
            errorLogMsg: The message to log on validation failure

        Returns:  `True` if good else `False`
        """
        try:
            floatValue: float = float(value)
            return self._isValidValue(value=floatValue, low=low, high=high)
        except ValueError as ve:
            self.logger.error(f'{errorLogMsg}: {ve}')
            return False

    def _isValidValue(self, value: float, low: float, high: float) -> bool:
        """
        Can use common comparisons for float or int
        Args:
            value:   The value to test
            low:     The smallest value it can be
            high:    The largest value it can be

        Returns:  `True` if in range else `False`
        """
        if low <= value <= high:
            return True
        else:
            return False
