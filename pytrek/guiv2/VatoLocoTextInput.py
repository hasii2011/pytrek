
from typing import Dict

from logging import Logger
from logging import getLogger

from arcade import SpriteSolidColor

from arcade import draw_text
from arcade import start_render

from arcade.color import BLACK
from arcade.color import RED
from arcade.color import WHITE

from arcade import key as arcadeKey

from arcade.gui import UIManager

from pytrek.guiv2.BaseSection import BaseSection

DEFAULT_INPUT_HEIGHT:   int = 20
DEFAULT_SECTION_HEIGHT: int = DEFAULT_INPUT_HEIGHT * 2
DEFAULT_SECTION_WIDTH:  int = 200


LEFT_MARGIN:   int = 10
RIGHT_MARGIN:  int = 10
BOTTOM_MARGIN: int = 10
TOP_MARGIN:    int = 0


PressedKeyToCharacter: Dict[int, str] = {
    arcadeKey.A: 'a',
    arcadeKey.B: 'b',
    arcadeKey.C: 'c',
    arcadeKey.D: 'd',
    arcadeKey.E: 'e',
    arcadeKey.F: 'f',
    arcadeKey.G: 'g',
    arcadeKey.H: 'h',
    arcadeKey.I: 'i',
    arcadeKey.J: 'j',
    arcadeKey.K: 'k',
    arcadeKey.L: 'l',
    arcadeKey.M: 'm',
    arcadeKey.N: 'n',
    arcadeKey.O: 'o',
    arcadeKey.P: 'p',
    arcadeKey.Q: 'q',
    arcadeKey.R: 'r',
    arcadeKey.S: 's',
    arcadeKey.T: 't',
    arcadeKey.U: 'u',
    arcadeKey.V: 'v',
    arcadeKey.W: 'w',
    arcadeKey.X: 'x',
    arcadeKey.Y: 'y',
    arcadeKey.Z: 'z',
    arcadeKey.NUM_0: '0',
    arcadeKey.NUM_1: '1',
    arcadeKey.NUM_2: '2',
    arcadeKey.NUM_3: '3',
    arcadeKey.NUM_4: '4',
    arcadeKey.NUM_5: '5',
    arcadeKey.NUM_6: '6',
    arcadeKey.NUM_7: '7',
    arcadeKey.NUM_8: '8',
    arcadeKey.NUM_9: '9',
    arcadeKey.KEY_0: '0',
    arcadeKey.KEY_1: '1',
    arcadeKey.KEY_2: '2',
    arcadeKey.KEY_3: '3',
    arcadeKey.KEY_4: '4',
    arcadeKey.KEY_5: '5',
    arcadeKey.KEY_6: '6',
    arcadeKey.KEY_7: '7',
    arcadeKey.KEY_8: '8',
    arcadeKey.KEY_9: '9',
    arcadeKey.SPACE:  ' ',
    arcadeKey.ENTER:  '',
    arcadeKey.RETURN: '',
}

TEXT_TOP_MARGIN:  int = 5
TEXT_LEFT_MARGIN: int = 2


class VatoLocoTextInput(BaseSection):
    """
    Super simple simulated text input.  I can't get UIInputText to work correctly in a section.

    See https://stackoverflow.com/questions/75944415/why-my-button-in-python-arcade-section-seems-inactive/78872518#78872518

    This limited text input does not support a text input caret;  It does not support inline editting

    """
    def __init__(self, left: int, bottom: int, width: int = DEFAULT_SECTION_WIDTH, height: int = DEFAULT_SECTION_HEIGHT, **kwargs):

        sectionLeft:   int = left + LEFT_MARGIN
        sectionBottom: int = bottom + BOTTOM_MARGIN
        sectionWidth:  int = width - LEFT_MARGIN - RIGHT_MARGIN

        super().__init__(left=sectionLeft, bottom=sectionBottom, width=sectionWidth, height=height, **kwargs)

        self.logger: Logger = getLogger(__name__)

        self._uiManager: UIManager = UIManager()

        self._hasFocus: bool = False
        self._value:    str  = ''

        inputWidth  = self.width // 2
        inputHeight = DEFAULT_INPUT_HEIGHT

        self._inputText: SpriteSolidColor = SpriteSolidColor(width=inputWidth, height=inputHeight, color=WHITE)

        self._inputText.position = self.left + self.width / 2, self.bottom + self.height / 2

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    def on_draw(self):
        start_render()
        self._uiManager.draw()
        super().on_draw()

        # self._drawInputArea()
        self._inputText.draw()
        if self._hasFocus is True:
            self._inputText.draw_hit_box(color=RED)

        draw_text(self._value,
                  start_x=self._inputText.left + TEXT_LEFT_MARGIN,
                  start_y=(self._inputText.bottom - TEXT_TOP_MARGIN) + self._inputText.height / 2,
                  width=int(self._inputText.width),
                  color=BLACK)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """
        Check if the button is pressed
         """
        if self._inputText.collides_with_point((x, y)):
            self.logger.info(f'Pressed inside text')
            self._hasFocus = True
        else:
            self._hasFocus = False

    def on_key_press(self, symbol: int, modifiers: int):
        if self._hasFocus:
            if symbol == arcadeKey.BACKSPACE:
                self._value = self._value[:-1]
            else:
                try:
                    letter: str = PressedKeyToCharacter[symbol]
                    if modifiers == arcadeKey.MOD_SHIFT:
                        letter = letter.upper()
                    self._value = f'{self._value}{letter}'
                except KeyError:
                    pass    # Only handle letters

        self.logger.info(f'{self._value=}')
