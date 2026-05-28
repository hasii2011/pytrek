
from typing import Callable

from logging import Logger
from logging import getLogger

from copy import copy as stdlibCopy

from arcade import color

from arcade.gui import UIEvent
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UIBoxLayout
from arcade.gui import UIInputText
from arcade.gui import UIKeyPressEvent
from arcade.gui import UIAnchorLayout

from arcade import key as arcadeKey

from pytrek.gui.BaseSection import BaseSection

from pytrek.Constants import COMMAND_SECTION_HEIGHT


LABEl_FONT_SIZE: int = 12
INPUT_HEIGHT:    int = 32
INPUT_WIDTH:     int = 200

INPUT_FIELD_BORDER_WIDTH: int = 2

# Margins
LEFT_MARGIN:  int = 10
RIGHT_MARGIN: int = 10

CommandEnteredCallback = Callable[[str], None]


class CommandInputText(UIInputText):

    def __init__(self, commandEnteredCallback: CommandEnteredCallback, **kwargs):
        """

        Args:
            commandEnteredCallback:
            **kwargs:
        """
        super().__init__(**kwargs)
        self._callback: CommandEnteredCallback = commandEnteredCallback

    def on_event(self, event: UIEvent) -> bool | None:

        if isinstance(event, UIKeyPressEvent):
            if event.symbol in (arcadeKey.ENTER, arcadeKey.RETURN):
                capturedText = self.text
                self.text = ''
                self._callback(capturedText)
                return True

        return super().on_event(event)

    def do_render_focus(self, surface):
        """
        Override to disable the default white focus outline.
        Antigravity did some hard work for me to find this;  I do NOT
        feel as dirty anymore
        """
        pass  # Removes the default 4px white focus outline completely

class CommandInputSection(BaseSection):
    """
    Renders and manages the command input UI section at the bottom of the screen.

    Functionality:
    1. Text Input and Layout:
       - Uses CommandInputText (subclass of arcade.gui.UIInputText) and a UILabel containing 'Enter Command'.
       - Arranges the widgets horizontally using a UIBoxLayout centered vertically within the section area.
       - Styles the text field with a white background and a black text/caret.
    2. Input Capture:
       - Overrides on_event inside the text input to intercept key presses.
       - When the user presses the Enter or Return key, it extracts the entered command, clears the field, and executes the callback.
    3. Event and Focus Lifecycle:
       - Manages an internal UIManager to route window-level input events.
       - Enables the UIManager and focuses the text field when shown, and disables the UIManager when hidden.
    """
    def __init__(self, left: int, bottom: int, commandEnteredCallback: CommandEnteredCallback, **kwargs):
        """

        Args:
            left:
            bottom:
            commandEnteredCallback:
            **kwargs:
        """
        self._callback: CommandEnteredCallback = commandEnteredCallback

        # Set up section boundaries
        sectionLeft:   int = left + LEFT_MARGIN
        sectionBottom: int = bottom
        sectionWidth:  int = self.window.width - LEFT_MARGIN - RIGHT_MARGIN - left
        sectionHeight: int = COMMAND_SECTION_HEIGHT

        super().__init__(left=sectionLeft, bottom=sectionBottom, width=sectionWidth, height=sectionHeight, **kwargs)

        self.logger:     Logger    = getLogger(__name__)
        self._uiManager: UIManager = UIManager()

        anchorLayout: UIAnchorLayout = UIAnchorLayout(x=5)
        hBox:         UIBoxLayout    = UIBoxLayout(vertical=False, align='center')

        self._label: UILabel = UILabel(text='Enter Command:', font_size=LABEl_FONT_SIZE, text_color=color.WHITE)

        # Create a copy of the default style for all states
        customStyle = {
            state: stdlibCopy(style_obj)
            for state, style_obj in UIInputText.DEFAULT_STYLE.items()
        }
        # Set the border width to 0 for all states in our copy
        for state_style in customStyle.values():
            state_style.border_width = 1

        # noinspection SpellCheckingInspection
        self._inputField: CommandInputText = CommandInputText(
            commandEnteredCallback=self._onCommandEntered,
            text='',
            width=INPUT_WIDTH,
            text_color=color.WHITE,
            caret_color=color.WHITE,
            font_name=('Andale Mono', 'Menlo', 'PT Mono', 'SF Mono'),
            style=customStyle
        )

        hBox.add(self._label.with_padding(right=20))
        hBox.add(self._inputField)

        alignY: int = (COMMAND_SECTION_HEIGHT - INPUT_HEIGHT) // 2
        anchorLayout.add(hBox, anchor_x='left', align_x=sectionLeft, anchor_y='bottom', align_y=alignY)

        self._uiManager.add(anchorLayout)

    def _onCommandEntered(self, command: str):
        self.logger.info(f'Command entered: {command}')
        self._callback(command)

    def on_draw(self):
        self.drawDebug()
        self._uiManager.draw()

    def on_show_section(self):
        self._uiManager.enable()
        self._inputField.focused = True

    def on_hide_section(self):
        self._uiManager.disable()
