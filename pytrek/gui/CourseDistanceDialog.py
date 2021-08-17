
from typing import Callable
from typing import Optional
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import View
from arcade import color
from arcade import key
from arcade import start_render

from arcade.gui import UIFlatButton
from arcade.gui import UIInputBox
from arcade.gui import UILabel
from arcade.gui import UIManager

from arcade.gui.ui_style import UIStyle


FONT_SIZE:  int = 12
LABEL_WIDTH: int = 125
INPUT_WIDTH: int = 150

FONT_COLOR = color.BLACK
BG_COLOR   = color.WHITE


class DialogButton(UIFlatButton):
    ID_OK:     str = '6666'
    ID_CANCEL: str = '7976'

    def __init__(self, text: str,
                 center_x: int = 0,
                 center_y: int = 0,
                 width:  int = 0,
                 height: int = 0,
                 align:  str = "center",
                 buttonId: Optional[str] = None,
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
    Main application class.
    """

    MADE_UP_PRETTY_MAIN_NAME: str = "TestGetCourseDistance"

    def __init__(self,):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._uiManager:     UIManager = UIManager()

        self._distanceInput: UIInputBox = cast(UIInputBox, None)
        self._courseInput:   UIInputBox = cast(UIInputBox, None)

    def setup(self):
        """
        Set up test program here
        """
        self._uiManager.purge_ui_elements()

        labelX: int = 75
        inputX: float = labelX + LABEL_WIDTH + 20
        ySlot:  int = self.window.height // 4

        self._createCourseControls(inputX, labelX, ySlot)
        self._createDistanceControls(inputX, labelX, ySlot)

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

        okColumnX:     int = 2 * self.window.width // 4
        cancelColumnX: int = 3 * self.window.width // 4

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
        self.logger.info(f"Clicked 'Ok'")

    def _onCancel(self):
        self.logger.info(f"Clicked 'Cancel'")
