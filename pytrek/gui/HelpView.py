
from typing import Dict
from typing import Callable

from logging import Logger
from logging import getLogger

from collections import namedtuple

from arcade import Texture
from arcade import View
from arcade import Window
from arcade import color

from arcade.gui import UIAnchorWidget
from arcade.gui import UIBoxLayout
from arcade.gui import UILabel
from arcade.gui import UIManager
from arcade.gui import UIMouseScrollEvent
from arcade.gui import UIOnClickEvent
from arcade.gui import UIPadding
from arcade.gui import UITextArea
from arcade.gui import UITextureButton
from arcade.gui import UITexturePane

from arcade import start_render
from arcade import load_texture

from arcade import key as arcadeKey

from pytrek.LocateResources import LocateResources

CreateTextResponse = namedtuple('CreateTextResponse', 'textArea, texturePane')


class HelpView(View):

    FONT_NAME: str = 'UniverseCondensed'

    def __init__(self, window: Window, completeCallback: Callable):

        super().__init__(window=window)

        self.logger:            Logger   = getLogger(__name__)
        self._completeCallback: Callable = completeCallback

        self._uiManager: UIManager = UIManager()

        self._uiManager.enable()

        window.background_color = color.BLUE_YONDER

        title:               UILabel        = self._createLabel(text='PyArcadeStarTrek Help', height=24, fontSize=18)
        createTextResponse: CreateTextResponse  = self._createHelpTextArea()

        wrappedHelpTextArea: UITexturePane = createTextResponse.texturePane
        self._helpTextArea:  UITextArea    = createTextResponse.textArea

        padding:   UIPadding = UIPadding(child=wrappedHelpTextArea, padding=(4, 4, 4, 4))
        buttonBox: UIBoxLayout = self._createScrollButtonContainer()

        hBox: UIBoxLayout = UIBoxLayout(vertical=False,
                                        children=[
                                            padding.with_border(width=2, color=color.WHITE).with_space_around(bottom=10, top=10),
                                            buttonBox.with_space_around(left=15, top=20),
                                        ])

        okButton: UITextureButton = self._createOkButton()
        mainBox: UIBoxLayout = UIBoxLayout(vertical=True,
                                           children=[
                                               title.with_space_around(top=20),
                                               hBox,
                                               okButton
                                           ])

        self._uiManager.add(
            UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="top",
                child=mainBox)
        )

    def on_draw(self):
        """
        Draw this view
        """
        start_render()
        self._uiManager.draw()

    def on_key_release(self, releasedKey: int, key_modifiers: int):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if releasedKey == arcadeKey.Q:
            import os
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            os._exit(0)

    def _createLabel(self, text: str = '', height: int = 16, fontSize: int = 12) -> UILabel:

        uiLabel: UILabel = UILabel(text=text, font_name=HelpView.FONT_NAME, height=height, font_size=fontSize, bold=True)
        return uiLabel

    def _createScrollButtonContainer(self) -> UIBoxLayout:

        upButton:   UITextureButton = self._createTextureButton(bareFileName='ArrowUp')
        downButton: UITextureButton = self._createTextureButton(bareFileName='ArrowDown')

        buttonBox: UIBoxLayout = UIBoxLayout(vertical=True,
                                             children=[
                                                 upButton.with_space_around(top=20),
                                                 downButton.with_space_around(bottom=10, top=10)
                                             ])

        @upButton.event('on_click')
        def onClickUp(event: UIOnClickEvent):
            self._onClickUp(event)

        @downButton.event('on_click')
        def onClickDown(event: UIOnClickEvent):
            self._onClickDown(event)

        return buttonBox

    def _createHelpTextArea(self) -> CreateTextResponse:
        """
        Creates and loads the help text

        Returns:  A named tuple that has the texture pane and the text area widgets
        """
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.RESOURCES_PACKAGE_NAME,
                                                           bareFileName='Help.txt')
        with open(fqFileName) as fd:
            lines: str = fd.read()
        textArea: UITextArea = UITextArea(width=550, height=360,
                                          text=lines,
                                          text_color=color.BLACK,
                                          font_name=HelpView.FONT_NAME)

        textureFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                                bareFileName='GreyPanel.png')
        background: Texture = load_texture(textureFileName)

        texturePane: UITexturePane = UITexturePane(
            textArea.with_space_around(right=20),
            tex=background,
            padding=(10, 10, 10, 10)
        )
        return CreateTextResponse(textArea=textArea, texturePane=texturePane)

    def _createTextureButton(self, bareFileName: str) -> UITextureButton:

        normalFileName:  str = f'{bareFileName}.png'
        pressedFileName: str = f'{bareFileName}Pressed.png'
        hoveredFileName: str = f'{bareFileName}Hovered.png'

        fqNormalFileName:  str = LocateResources.getResourcesPath(LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=normalFileName)
        fqPressedFileName: str = LocateResources.getResourcesPath(LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=pressedFileName)
        fqHoveredFileName: str = LocateResources.getResourcesPath(LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=hoveredFileName)

        normalTexture:  Texture = load_texture(fqNormalFileName)
        pressedTexture: Texture = load_texture(fqPressedFileName)
        hoveredTexture: Texture = load_texture(fqHoveredFileName)

        button: UITextureButton = UITextureButton(texture=normalTexture,
                                                  texture_pressed=pressedTexture,
                                                  texture_hovered=hoveredTexture,
                                                  width=32, height=32)

        return button

    def _createOkButton(self) -> UITextureButton:

        buttonFileName:        str = LocateResources.getResourcesPath(LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='HelpOkButton.png')
        pressedButtonFileName: str = LocateResources.getResourcesPath(LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='HelpOkButtonPressed.png')
        hoveredButtonFileName: str = LocateResources.getResourcesPath(LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='HelpOkButtonHovered.png')

        okButtonTexture:        Texture = load_texture(buttonFileName)
        okButtonPressedTexture: Texture = load_texture(pressedButtonFileName)
        okButtonHoveredTexture: Texture = load_texture(hoveredButtonFileName)

        buttonStyle: Dict = {'font_name': 'arial',
                             'font_size': 12
                             }

        okButton: UITextureButton = UITextureButton(width=35, height=35,
                                                    texture=okButtonTexture,
                                                    texture_pressed=okButtonPressedTexture,
                                                    texture_hovered=okButtonHoveredTexture,
                                                    style=buttonStyle)

        @okButton.event('on_click')
        def onClickOk(event: UIOnClickEvent):
            self._onClickOk(event)

        return okButton

    def _onClickUp(self, event: UIOnClickEvent):
        self.__scrollHelp(event, -2)

    def _onClickDown(self, event: UIOnClickEvent):
        self.__scrollHelp(event, 2)

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
        x = self._helpTextArea.center_x
        y = self._helpTextArea.center_y

        mouseEvent: UIMouseScrollEvent = UIMouseScrollEvent(source=event.source, scroll_y=scroll_y, scroll_x=0, x=x, y=y)
        self._helpTextArea.on_event(mouseEvent)
