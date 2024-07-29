
from typing import Callable

from logging import Logger
from logging import getLogger
from typing import Dict
from typing import cast

from arcade import Texture
from arcade import load_texture

from arcade.gui import UIBoxLayout
from arcade.gui import UIOnClickEvent
from arcade.gui import UITextureButton

from pytrek.LocateResources import LocateResources


class ResourceCache:

    cachedButtonBox: UIBoxLayout = cast(UIBoxLayout, None)

    okButtonTexture:            Texture = cast(Texture, None)
    okButtonPressedTexture:     Texture = cast(Texture, None)
    cancelButtonTexture:        Texture = cast(Texture, None)
    cancelButtonPressedTexture: Texture = cast(Texture, None)

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    @classmethod
    def createDialogButtons(cls, okCallback: Callable, cancelCallback: Callable) -> UIBoxLayout:
        """
        Creates and binds the dialog 'Ok' and 'Cancel' buttons

        Returns:  The button box container
        """

        if cls.okButtonTexture is None:
            ResourceCache.loadButtonTextures()

        buttonBox:  UIBoxLayout = UIBoxLayout(vertical=False)
        buttonStyle: Dict = {'font_name': 'arial',
                             'font_size': 12
                             }
        okButton: UITextureButton = UITextureButton(width=35, height=35,
                                                    texture=cls.okButtonTexture, texture_pressed=cls.okButtonPressedTexture,
                                                    style=buttonStyle)

        cancelButton: UITextureButton = UITextureButton(width=35, height=35,
                                                        texture=cls.cancelButtonTexture, texture_pressed=cls.cancelButtonPressedTexture,
                                                        style=buttonStyle)

        buttonBox.add(okButton.with_space_around(top=10, bottom=10, left=5))
        buttonBox.add(cancelButton.with_space_around(top=10, bottom=10, left=5, right=5))

        @okButton.event('on_click')
        def onClickOk(event: UIOnClickEvent):
            okCallback(event)

        @cancelButton.event('on_click')
        def onClickCancel(event: UIOnClickEvent):
            cancelCallback(event)

        return buttonBox

    @classmethod
    def loadButtonTextures(cls):

        okFileName:            str = LocateResources.getImagePath(bareFileName='OkButtonNormal-512.png')
        okPressedFileName:     str = LocateResources.getImagePath(bareFileName='OkButtonPressed-512.png')
        cancelFileName:        str = LocateResources.getImagePath(bareFileName='CancelButtonNormal-512.png')
        cancelPressedFileName: str = LocateResources.getImagePath(bareFileName='CancelButtonPressed-512.png')

        cls.okButtonTexture            = load_texture(okFileName)
        cls.okButtonPressedTexture     = load_texture(okPressedFileName)
        cls.cancelButtonTexture        = load_texture(cancelFileName)
        cls.cancelButtonPressedTexture = load_texture(cancelPressedFileName)
