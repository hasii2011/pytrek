
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
from arcade import key
from arcade import load_texture
from arcade import start_render

from arcade.gui import UIFlatButton
from arcade.gui import UIInputBox
from arcade.gui import UILabel
from arcade.gui import UIManager

from arcade.gui.ui_style import UIStyle

from pytrek.Constants import CONSOLE_HEIGHT
from pytrek.Constants import MAXIMUM_COURSE_VALUE
from pytrek.Constants import MAXIMUM_DISTANCE_VALUE
from pytrek.Constants import MINIMUM_COURSE_VAlUE
from pytrek.Constants import MINIMUM_DISTANCE_VALUE
from pytrek.Constants import QUADRANT_GRID_HEIGHT

from pytrek.LocateResources import LocateResources

from tests.TestSpriteSheet import SCREEN_WIDTH

FONT_SIZE:  int = 12
LABEL_WIDTH: int = 125
INPUT_WIDTH: int = 150

FONT_COLOR = color.BLACK
BG_COLOR   = color.WHITE


class DialogAnswer(Enum):
    Cancelled = 'Cancelled'
    Ok = 'Ok'


@dataclass
class CourseDistanceAnswer:
    """
    The `course` and `distance` values are only valid when dialogAnswer is DialogAnswer.Ok
    """
    dialogAnswer: DialogAnswer = DialogAnswer.Cancelled

    course:   int = 0
    distance: int = 0


# DialogCallback = NewType('DialogCallback', Callable[[CourseDistanceAnswer], None])
DialogCallback = Callable[[CourseDistanceAnswer], None]


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


class CourseDistanceDialog(View):
    """
    Presents a 'pseudo' dialog like UI in order to gather a course and distance value for manual warp
    travel;  Does validation on input and only proceeds if valid input is presented or the player
    cancels the interaction
    """
    INVALID_DISTANCE_MESSAGE: str = 'Invalid (1-9)'
    INVALID_COURSE_MESSAGE:   str = 'Invalid (1-12)'

    LEN_INVALID_DISTANCE_MESSAGE: int = len(INVALID_DISTANCE_MESSAGE)
    LEN_INVALID_COURSE_MESSAGE:   int = len(INVALID_COURSE_MESSAGE)

    def __init__(self, completeCallback: DialogCallback):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._completeCallback: DialogCallback = completeCallback

        self._uiManager:     UIManager  = UIManager()
        self._distanceInput: UIInputBox = cast(UIInputBox, None)
        self._courseInput:   UIInputBox = cast(UIInputBox, None)
        self._course:        str        = ''
        self._distance:      str        = ''

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='QuadrantBackground.png')
        self._background = load_texture(fqFileName)

    def setup(self):
        """
        Set up test program here
        """
        self._uiManager.purge_ui_elements()

        labelX: int = 75
        inputX: float = labelX + LABEL_WIDTH + 20
        ySlot:  int = self.window.height // 16

        self._courseInput   = self._createCourseControls(inputX, labelX, ySlot)
        self._distanceInput = self._createDistanceControls(inputX, labelX, ySlot)

        self._createDialogButtons(ySlot=ySlot)

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

    def on_key_press(self, pressedKey: int, key_modifiers: int):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://arcade.academy/arcade.key.html
        """
        if pressedKey == key.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)

    def _createDistanceControls(self, inputX: float, labelX: int, ySlot: int) -> UIInputBox:
        """

        Args:
            inputX:     x point of courseInput
            labelX:     x point of label
            ySlot:      The y slot position

        Returns:  The distance UIInputBox
        """
        distanceLabel: UILabel     = self._createLabel(text='Distance:', centerX=labelX, centerY=ySlot * 2, width=LABEL_WIDTH)
        distanceInput: UIInputBox = UIInputBox(center_x=inputX, center_y=ySlot * 2, width=150)
        self._setInputStyle(distanceInput)

        self._uiManager.add_ui_element(distanceLabel)
        self._uiManager.add_ui_element(distanceInput)

        return distanceInput

    def _createCourseControls(self, inputX: float, labelX: int, ySlot: int) -> UIInputBox:
        """

        Args:
            inputX:     x point of courseInput
            labelX:     x point of label
            ySlot:      The y slot position

        Returns:  The course UIInputBox
        """

        courseLabel: UILabel    = self._createLabel(text='Course:', centerX=labelX, centerY=ySlot * 3, width=LABEL_WIDTH)
        courseInput: UIInputBox = UIInputBox(center_x=inputX, center_y=ySlot * 3, width=150)
        self._setInputStyle(courseInput)

        self._uiManager.add_ui_element(courseLabel)
        self._uiManager.add_ui_element(courseInput)

        return courseInput

    def _createLabel(self, text: str, centerX: float, centerY: float, width: int) -> UILabel:

        label: UILabel = UILabel(text=text, center_x=centerX, center_y=centerY, width=width)
        self._setLabelStyle(label)

        return label

    def _createDialogButtons(self, ySlot: int):

        okColumnX:     int = 2 * self.window.width // 12
        cancelColumnX: int = 4 * self.window.width // 12

        okButton: DialogButton = DialogButton('Ok', callback=self._onOk, buttonId=DialogButton.ID_OK, center_x=okColumnX, center_y=ySlot * 1, width=80)
        self._setButtonStyle(dlgButton=okButton)

        cancelButton: DialogButton = DialogButton('Cancel', callback=self._onCancel, buttonId=DialogButton.ID_CANCEL, center_x=cancelColumnX,
                                                  center_y=ySlot * 1, width=80)
        self._setButtonStyle(dlgButton=cancelButton)

        self._uiManager.add_ui_element(okButton)
        self._uiManager.add_ui_element(cancelButton)

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

        self._course   = self._courseInput.text
        self._distance = self._distanceInput.text

        valid: bool = self._validateCourse(self._course)
        if valid is True:
            valid = self._validateDistance(self._distance)
            if valid is True:
                answer: CourseDistanceAnswer = CourseDistanceAnswer(course=self._course, distance=self._distance, dialogAnswer=DialogAnswer.Ok)
                self._completeCallback(answer)
            else:
                self._distanceInput.text = CourseDistanceDialog.INVALID_DISTANCE_MESSAGE
                self._distanceInput.cursor_index = CourseDistanceDialog.LEN_INVALID_DISTANCE_MESSAGE
        else:
            self._courseInput.text = CourseDistanceDialog.INVALID_COURSE_MESSAGE
            self._courseInput.cursor_index = CourseDistanceDialog.LEN_INVALID_COURSE_MESSAGE

        self.logger.info(f"{self._course=} {self._distance=}")

    def _onCancel(self):
        self.logger.info(f"Clicked 'Cancel'")
        answer: CourseDistanceAnswer = CourseDistanceAnswer(course=-1, distance=-1, dialogAnswer=DialogAnswer.Cancelled)

        self._completeCallback(answer)

    def _validateCourse(self, course: str) -> bool:
        return self._validateValue(value=course, low=MINIMUM_COURSE_VAlUE, high=MAXIMUM_COURSE_VALUE, errorLogMsg='Course Input error: ')

    def _validateDistance(self, distance: str) -> bool:
        return self._validateValue(value=distance, low=MINIMUM_DISTANCE_VALUE, high=MAXIMUM_DISTANCE_VALUE, errorLogMsg='Distance Input error: ')

    def _validateValue(self, value: str, low: int, high: int, errorLogMsg: str) -> bool:
        """
        Args:
            value:   The string value
            low:     The smallest integer it can be
            high:    The largest integer it can be
            errorLogMsg: The message to log on validation failure

        Returns:  `True` if good else `False`
        """
        try:
            intValue: int = int(value)
            if low <= intValue <= high:
                return True
            else:
                return False
        except ValueError as ve:
            self.logger.error(f'{errorLogMsg}: {ve}')
            return False
