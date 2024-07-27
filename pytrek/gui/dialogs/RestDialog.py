
from typing import Callable
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from arcade import Texture
from arcade import View
from arcade import color

from arcade import load_texture
from arcade import start_render

from arcade.gui import UIAnchorWidget
from arcade.gui import UIBoxLayout
from arcade.gui import UIInputText
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UIOnClickEvent
from arcade.gui import UISpace

from pytrek.gui.dialogs.DlgConstants import DialogAnswer
from pytrek.gui.dialogs.ResourceCache import ResourceCache
from pytrek.gui.dialogs.StdMsgBox import StdMsgBox

from pytrek.LocateResources import LocateResources


@dataclass
class RestAnswer:
    """
    The `restDates` value is only valid when dialogAnswer is DialogAnswer.Ok
    """
    dialogAnswer: DialogAnswer = DialogAnswer.Cancelled
    restDates:    int          = -1


RestCallback = Callable[[RestAnswer], None]


class RestDialog(View):

    REST_ERROR_MESSAGE: str = 'Star dates must be an integer value'

    def __init__(self, completeCallback: RestCallback):
        super().__init__()
        self._completeCallback: Callable = completeCallback

        self.logger: Logger = getLogger(__name__)

        self._uiManager: UIManager = UIManager()
        self._uiManager.enable()

        self._restStarDates:  UIInputText = cast(UIInputText, None)

        fqFileName: str = LocateResources.getImagePath(bareFileName='EmptySpace.png')

        self._inputTexture: Texture = load_texture(fqFileName)

        # Create a vertical BoxGroup to align label text items
        self._vBox: UIBoxLayout = UIBoxLayout(vertical=True)
        self._restInput:       UIInputText = cast(UIInputText, None)
        restStarDatesInputBox: UIBoxLayout = self._createRestStarDatesInputBox()
        buttonBox:             UIBoxLayout = ResourceCache.createDialogButtons(okCallback=self._onClickOk, cancelCallback=self._onClickCancel)

        self._vBox.add(UISpace(height=50))
        self._vBox.add(restStarDatesInputBox.with_border(width=5, color=color.WHITE).with_space_around(bottom=10))
        self._vBox.add(buttonBox.with_border(width=3, color=color.WHITE))

        self._uiManager.add(
            UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="top",
                align_y=10,
                child=self._vBox)
        )

    def on_draw(self):
        start_render()
        self._uiManager.draw()

    def _createRestStarDatesInputBox(self) -> UIBoxLayout:

        restStarDatesInputBox: UIBoxLayout = UIBoxLayout(vertical=False, align='x:right, y:center')

        restLabel: UILabel     = self._createLabel(text='Number of Star Dates to rest: ')
        restInput: UIInputText = UIInputText(text='5', height=18, width=100, font_size=12, text_color=color.BLACK)

        restStarDatesInputBox.add(
            restLabel.with_space_around(left=5, top=5, bottom=5)
        )
        restStarDatesInputBox.add(restInput
                                  # .with_border(width=2, color=color.WHITE)
                                  .with_space_around(left=5, right=5, top=10)
                                  .with_background(texture=self._inputTexture)
                                  )

        self._restInput = restInput
        return restStarDatesInputBox

    def _createLabel(self, text: str = '') -> UILabel:

        uiLabel: UILabel = UILabel(text=text, font_name='arial', height=16, font_size=12, bold=True)

        return uiLabel

    # noinspection PyUnusedLocal
    def _onClickOk(self, event: UIOnClickEvent):

        restDates:  str = self._restInput.text
        try:
            intRest: int = int(restDates)
            restAnswer: RestAnswer = RestAnswer(dialogAnswer=DialogAnswer.Ok, restDates=intRest)
            self._completeCallback(restAnswer)
        except ValueError as e:
            StdMsgBox.displayMessageBox(uiManager=self._uiManager, msg=RestDialog.REST_ERROR_MESSAGE)
            self.logger.error(f'{e}')

    # noinspection PyUnusedLocal
    def _onClickCancel(self, event: UIOnClickEvent):
        self._completeCallback(RestAnswer())
