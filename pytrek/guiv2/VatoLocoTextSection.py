
from typing import Callable
from typing import Dict

from logging import Logger
from logging import getLogger

from arcade import SpriteSolidColor
from arcade import Text

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

# Section Margins
LEFT_MARGIN:   int = 10
RIGHT_MARGIN:  int = 10
BOTTOM_MARGIN: int = 10
# TOP_MARGIN:    int = 0

TEXT_TOP_MARGIN:  int = 5
TEXT_LEFT_MARGIN: int = 2

LABEL_LEFT_MARGIN: int = 10

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

ReturnKeyPressedCallback = Callable[[str], None]

LABEL_TEXT:      str  = 'Enter Command: '
LABEL_FONT_SIZE: int = 12

DEBUG:      bool = False


class VatoLocoTextSection(BaseSection):
    """
    Super simple simulated text input.  I can't get UIInputText to work correctly in a section.

    See https://stackoverflow.com/questions/75944415/why-my-button-in-python-arcade-section-seems-inactive/78872518#78872518

    This limited text input does not support a text input caret;  It does not support inline editing.

    You can retrieve the current input by accessing the value property
    If you supply a `returnCallback`, that methods gets called when the user presses the `enter/return` key and passes
    it the supplied text.  It resets the text input value

    """
    def __init__(self, left: int, bottom: int, callback: ReturnKeyPressedCallback, **kwargs):

        self._callback: ReturnKeyPressedCallback = callback
        #
        # Set up the section size and location (opinionated)
        #
        sectionLeft:   int = left + LEFT_MARGIN
        sectionBottom: int = bottom + BOTTOM_MARGIN
        sectionWidth:  int = self.window.width - LEFT_MARGIN - RIGHT_MARGIN - left
        sectionHeight: int = DEFAULT_SECTION_HEIGHT

        super().__init__(left=sectionLeft, bottom=sectionBottom, width=sectionWidth, height=sectionHeight, **kwargs)

        self.logger:     Logger    = getLogger(__name__)
        self._uiManager: UIManager = UIManager()
        self._hasFocus:  bool      = False
        self._value:     str       = ''

        labelX:        float = self.left + LABEL_LEFT_MARGIN
        labelAndTextY: float = self.bottom + self.height / 2

        self._label:             Text             = self._setupLabel(labelX=labelX, labelAndTextY=labelAndTextY)
        self._collisionDetector: SpriteSolidColor = self._setupTheCollisionDetector()

        detectorX: float = self._label.right + labelX + self._label.content_width
        self.logger.info(f'{self._label.right=}  {self._label.content_width=}   {labelX=}  {detectorX=}')
        self._collisionDetector.position = detectorX, labelAndTextY

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    def on_draw(self):
        start_render()
        self._uiManager.draw()

        if DEBUG is True:
            super().on_draw()
            self._label.draw_debug()

        self._label.draw()
        self._collisionDetector.draw()
        if self._hasFocus is True:
            self._collisionDetector.draw_hit_box(color=RED)

        # Draw the input value on top of the sprite
        draw_text(self._value,
                  start_x=self._collisionDetector.left + TEXT_LEFT_MARGIN,
                  start_y=(self._collisionDetector.bottom - TEXT_TOP_MARGIN) + self._collisionDetector.height / 2,
                  width=int(self._collisionDetector.width),
                  color=BLACK)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """
        Check if the button is pressed
         """
        if self._collisionDetector.collides_with_point((x, y)):
            self.logger.info(f'Pressed inside text')
            self._hasFocus = True
        else:
            self.logger.info(f'Pressed outside text')
            self._hasFocus = False

    def on_mouse_leave(self, x: int, y: int):
        self._hasFocus = False

    def on_key_press(self, symbol: int, modifiers: int):
        if self._hasFocus:
            if symbol == arcadeKey.BACKSPACE:
                self._value = self._value[:-1]
            elif symbol == arcadeKey.ENTER or symbol == arcadeKey.RETURN:
                self.logger.info(f'Return pressed')
                self._callback(self._value)
                self._value = ''
            else:
                try:
                    letter: str = PressedKeyToCharacter[symbol]
                    if modifiers == arcadeKey.MOD_SHIFT:
                        letter = letter.upper()
                    self._value = f'{self._value}{letter}'
                except KeyError:
                    self.logger.debug('Only handle letters')    # eat it

        self.logger.info(f'{self._value=}')

    def _setupTheCollisionDetector(self) -> SpriteSolidColor:
        """
        Use a sprite for easy hit collision computation with mouse click

        Returns: Our collision detecting immovable sprite
        """

        inputWidth  = self.width // 3
        inputHeight = DEFAULT_INPUT_HEIGHT
        collisionDetector: SpriteSolidColor = SpriteSolidColor(width=inputWidth, height=inputHeight, color=WHITE)

        return collisionDetector

    def _setupLabel(self, labelX: float, labelAndTextY: float) -> Text:

        labelY: float = labelAndTextY - TEXT_TOP_MARGIN
        width:  int   = LABEL_FONT_SIZE * len(LABEL_TEXT)
        label: Text = Text(text=LABEL_TEXT, start_x=labelX, start_y=labelY, width=width, color=WHITE)

        return label
