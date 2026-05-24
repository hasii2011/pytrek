
from typing import Callable

from logging import Logger
from logging import getLogger

from arcade import Texture
from arcade import View

from arcade import color

from arcade.gui import UIBoxLayout
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UIMouseScrollEvent
from arcade.gui import UIOnClickEvent
from arcade.gui import UIStyleBase
from arcade.gui import UITextArea
from arcade.gui import UITextureButton

from arcade import load_texture

from pytrek.LocateResources import LocateResources


class HelpView(View):

    # noinspection SpellCheckingInspection
    FONT_NAME: str = 'MonoFonto'

    def __init__(self, completeCallback: Callable):

        super().__init__()

        self.logger:            Logger   = getLogger(__name__)
        self._completeCallback: Callable = completeCallback

        self._uiManager: UIManager = UIManager()

        title:              UILabel    = self._createLabel(text='PyArcadeStarTrek Help', height=24, fontSize=18)
        self._helpTextArea: UITextArea = self._createHelpTextArea()

        buttonBox: UIBoxLayout = self._createScrollButtonContainer()

        hBox: UIBoxLayout = UIBoxLayout(vertical=False,
                                        children=[
                                            self._helpTextArea,
                                            buttonBox.with_padding(left=10, right=10, top=10, bottom=10).with_border(width=2, color=color.WHITE),
                                        ])

        okButton: UITextureButton = self._createOkButton()
        mainBox:  UIBoxLayout     = UIBoxLayout(vertical=True,
                                                children=[
                                                    title.with_padding(top=20),
                                                    hBox,
                                                    okButton
                                                ])

        from arcade.gui import UIAnchorLayout

        anchor_layout = UIAnchorLayout()
        anchor_layout.add(mainBox, anchor_x="center_x", anchor_y="top")
        self._uiManager.add(anchor_layout)

    def on_draw(self):
        """
        Draw this view
        """
        self.clear()
        self._uiManager.draw()

    def on_show_view(self):
        self._uiManager.enable()

    def on_hide_view(self):
        self._uiManager.disable()

    def _createLabel(self, text: str = '', height: int = 16, fontSize: int = 12) -> UILabel:

        uiLabel: UILabel = UILabel(text=text, font_name=HelpView.FONT_NAME, height=height, font_size=fontSize, bold=True)
        return uiLabel

    def _createScrollButtonContainer(self) -> UIBoxLayout:

        upButton:   UITextureButton = self._createTextureButton(bareFileName='ArrowUp')
        downButton: UITextureButton = self._createTextureButton(bareFileName='ArrowDown')

        buttonBox: UIBoxLayout = UIBoxLayout(vertical=True,
                                             children=[
                                                 upButton.with_padding(top=20),
                                                 downButton.with_padding(bottom=10, top=10)
                                             ])

        @upButton.event('on_click')
        def onClickUp(event: UIOnClickEvent):
            self._onClickUp(event)

        @downButton.event('on_click')
        def onClickDown(event: UIOnClickEvent):
            self._onClickDown(event)

        return buttonBox

    def _createHelpTextArea(self) -> UITextArea:
        """
        Creates and loads the help text

        Returns:  A named tuple that has the texture pane and the text area widgets
        """
        fqFileName: str = LocateResources.getResourcesPath(bareFileName='Help.txt',
                                                           resourcePath=LocateResources.RESOURCES_PATH,
                                                           packageName=LocateResources.RESOURCES_PACKAGE_NAME)
        with open(fqFileName) as fd:
            lines: str = fd.read()
        textArea: UITextArea = UITextArea(width=600, height=360,
                                          text=lines,
                                          text_color=color.BLACK,
                                          font_name=HelpView.FONT_NAME)

        textureFileName: str     = LocateResources.getImagePath(bareFileName='GreyPanel.png')
        background:      Texture = load_texture(textureFileName)

        # Chaining background and padding directly on the child or a layout widget

        textArea.with_padding(right=20).with_background(texture=background).with_padding(all=10)

        return textArea

    def _createTextureButton(self, bareFileName: str) -> UITextureButton:

        normalFileName:  str = f'{bareFileName}.png'
        pressedFileName: str = f'{bareFileName}Pressed.png'
        hoveredFileName: str = f'{bareFileName}Hovered.png'

        fqNormalFileName:  str = LocateResources.getImagePath(bareFileName=normalFileName)
        fqPressedFileName: str = LocateResources.getImagePath(bareFileName=pressedFileName)
        fqHoveredFileName: str = LocateResources.getImagePath(bareFileName=hoveredFileName)

        normalTexture:  Texture = load_texture(fqNormalFileName)
        pressedTexture: Texture = load_texture(fqPressedFileName)
        hoveredTexture: Texture = load_texture(fqHoveredFileName)

        button: UITextureButton = UITextureButton(texture=normalTexture,
                                                  texture_pressed=pressedTexture,
                                                  texture_hovered=hoveredTexture,
                                                  width=64, height=64)

        return button

    def _createOkButton(self) -> UITextureButton:

        buttonFileName:        str = LocateResources.getImagePath(bareFileName='HelpOkButton.png')
        pressedButtonFileName: str = LocateResources.getImagePath(bareFileName='HelpOkButtonPressed.png')
        hoveredButtonFileName: str = LocateResources.getImagePath(bareFileName='HelpOkButtonHovered.png')

        okButtonTexture:        Texture = load_texture(buttonFileName)
        okButtonPressedTexture: Texture = load_texture(pressedButtonFileName)
        okButtonHoveredTexture: Texture = load_texture(hoveredButtonFileName)

        # buttonStyle: Dict = {'font_name': 'arial',
        #                      'font_size': 12
        #                      }
        # Define styles for the required states
        buttonStyle: dict[str, UIStyleBase]  = {
            "normal": UITextureButton.UIStyle(font_name="arial", font_size=12),
            "hover": UITextureButton.UIStyle(font_name="arial", font_size=12),
            "press": UITextureButton.UIStyle(font_name="arial", font_size=12),
            "disabled": UITextureButton.UIStyle(font_name="arial", font_size=12),
        }

        okButton: UITextureButton = UITextureButton(width=35, height=35,
                                                    texture=okButtonTexture,
                                                    texture_pressed=okButtonPressedTexture,
                                                    texture_hovered=okButtonHoveredTexture,
                                                    style=buttonStyle
                                                    )

        @okButton.event('on_click')
        def onClickOk(event: UIOnClickEvent):
            self._onClickOk(event)

        return okButton

    def _onClickUp(self, event: UIOnClickEvent):
        self.__scrollHelp(event, -5)                # TODO: make this increment configurable

    def _onClickDown(self, event: UIOnClickEvent):
        self.__scrollHelp(event, 5)                 # TODO: make this increment configurable

    # noinspection PyUnusedLocal
    def _onClickOk(self, event: UIOnClickEvent):
        self._completeCallback()

    def __scrollHelp(self, event: UIOnClickEvent, scroll_y: int):
        """
        This is my hack to do scrolling.  I do not kno2 how to post an event on arcade's
        UI event queue;  Not sure if that is possible at this point

        Only scroll in the vertical direction

        Args:
            event:      Some UI event
            scroll_y:   How much to scroll;  Negative numbers scroll up
        """
        x: int = round(self._helpTextArea.center_x)
        y: int = round(self._helpTextArea.center_y)

        mouseEvent: UIMouseScrollEvent = UIMouseScrollEvent(source=event.source, scroll_y=scroll_y, scroll_x=0, x=x, y=y)
        self._helpTextArea.on_event(mouseEvent)
