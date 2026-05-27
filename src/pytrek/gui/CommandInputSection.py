
from typing import Callable

from logging import Logger
from logging import getLogger

from arcade import color
from arcade import key as arcadeKey

from arcade.gui import UIEvent
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UIBoxLayout
from arcade.gui import UIInputText
from arcade.gui import UIKeyPressEvent
from arcade.gui import UIAnchorLayout

from pytrek.gui.BaseSection import BaseSection

from pytrek.Constants import COMMAND_SECTION_HEIGHT


LABEl_FONT_SIZE: int = 12
INPUT_HEIGHT:    int = 30
INPUT_WIDTH:     int = 200

INPUT_FIELD_BORDER_WIDTH: int = 0

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


class CommandInputSection(BaseSection):

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

        self._label:      UILabel          = UILabel(text='Enter Command:', font_size=LABEl_FONT_SIZE, text_color=color.WHITE)
        self._inputField: CommandInputText = CommandInputText(
            commandEnteredCallback=self._onCommandEntered,
            text='',
            width=INPUT_WIDTH,
            height=INPUT_HEIGHT,
            text_color=color.WHITE,
            caret_color=color.WHITE,
            border_width=INPUT_FIELD_BORDER_WIDTH,
        ).with_background(color=color.BLACK)

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
