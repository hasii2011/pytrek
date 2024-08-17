
from typing import Callable
from typing import Optional
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Color
from arcade import Texture
from arcade import Window
from arcade import color
from arcade import load_texture
from arcade import start_render

from arcade.gui import UIAnchorWidget
from arcade.gui import UIBoxLayout
from arcade.gui import UIEvent
from arcade.gui import UIInputText
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UITextEvent

from pytrek.LocateResources import LocateResources

from pytrek.commandparser.CommandType import CommandType
from pytrek.commandparser.ParsedCommand import ParsedCommand
from pytrek.commandparser.CommandParser import CommandParser
from pytrek.commandparser.InvalidCommandException import InvalidCommandException
from pytrek.commandparser.InvalidCommandValueException import InvalidCommandValueException

from pytrek.guiv2.BaseSection import BaseSection

COMMAND_INPUT_HEIGHT: int = 20


class CommandInput(UIInputText):
    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 width: float = 100,
                 height: float = 50,
                 text: str = "",
                 font_name=('Arial',),
                 font_size: float = 12,
                 text_color: Color = (0, 0, 0, 255),
                 multiline=False,
                 size_hint=None,
                 size_hint_min=None,
                 size_hint_max=None,
                 style=None,
                 **kwargs
                 ):
        super().__init__(x=x, y=y, width=width, height=height,
                         text=text,
                         font_name=font_name, font_size=font_size, text_color=text_color,
                         multiline=multiline,
                         size_hint=size_hint,
                         size_hint_min=size_hint_min,
                         size_hint_max=size_hint_max,
                         style=style,
                         **kwargs
                         )
        self._callback: Callable = cast(Callable, None)

    def on_event(self, event: UIEvent) -> Optional[bool]:

        if self._active:
            if isinstance(event, UITextEvent):
                uiTextEvent: UITextEvent = cast(UITextEvent, event)
                self._callback(uiTextEvent.text)

        return super().on_event(event=event)

    def setTextEventCallback(self, cb: Callable):
        self._callback = cb


class CommandInputSection(BaseSection):

    HEIGHT:          int = COMMAND_INPUT_HEIGHT * 2
    POSITION_MARGIN: int = 20
    RETURN_KEY:      int = 13

    def __init__(self, left: int = 0, bottom: int = 0, **kwargs):

        window: Window = self.window
        w:      int    = window.width
        super().__init__(left=left, bottom=bottom, width=w, height=CommandInputSection.HEIGHT, **kwargs)

        self.logger:     Logger    = getLogger(__name__)
        self._uiManager: UIManager = UIManager()
        self._uiManager.enable()

        fqFileName: str = LocateResources.getImagePath(bareFileName='EmptySpace.png')

        self._inputTexture: Texture      = load_texture(fqFileName)
        self._commandInput: CommandInput = cast(CommandInput, None)

        commandInputLayout: UIBoxLayout = self._createCommandInput()

        self._commandInput.setTextEventCallback(self._handleCommandInput)

        # self._uiManager.add(
        #     UIAnchorWidget(
        #         # anchor_x='center_x',
        #         # anchor_y='center_y',
        #         align_x=0,
        #         align_y=0,
        #         child=commandInputLayout)
        # )
        self._uiManager.add(commandInputLayout)

        self._commandExtractor: CommandParser = CommandParser(asciiMode=True)

    def on_update(self, delta_time: float):
        self._commandInput.on_update(delta_time)

    def on_draw(self):
        start_render()
        self._uiManager.draw()
        super().on_draw()

    def _createCommandInput(self):
        """
        Sets the _commandInput variable

        Returns:  A box layout widget
        """

        layout:       UIBoxLayout  = UIBoxLayout(x=self.left + 10, y=self.top,
                                                 vertical=False, color=color.WHITE)
        commandLabel: UILabel      = self._createLabel(text='Enter Command: ')
        commandInput: CommandInput = CommandInput(text='aaaa', height=18, width=200, font_size=12, text_color=color.BLACK)

        layout.add(commandLabel.with_space_around(bottom=5, top=5))
        layout.add(commandInput.with_space_around(left=5)
                               .with_background(texture=self._inputTexture)
                   )

        self._commandInput = commandInput
        return layout

    def _handleCommandInput(self, key):

        self.logger.info(f'User entered: `{key}` {ord(key)=}')
        # if ord(key) == InputSection.RETURN_KEY:
        #     self._commandInput.text = ''
        try:
            parsedCommand: ParsedCommand = self._commandExtractor.processKeyPress(key)
            if parsedCommand.commandType != CommandType.NoCommand:
                self._commandInput.text = ''
                self._executeCommand(parsedCommand=parsedCommand)
        except InvalidCommandException as ice:
            self.logger.error(f'Invalid command: {ice}')        # TODO send message to message console or raise error view
            self._commandInput.text = ''
        except InvalidCommandValueException as e:
            self.logger.error(f'Invalid command value: {e}')     # TODO send message to message console or raise error view
            self._commandInput.text = ''

    def _executeCommand(self, parsedCommand: ParsedCommand):
        pass

    def _createLabel(self, text: str = '') -> UILabel:
        uiLabel: UILabel = UILabel(text=text, font_name='arial', height=16, font_size=12, bold=True)
        return uiLabel
