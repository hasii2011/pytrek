
from typing import cast

from uuid import uuid4

from pytrek.LocateResources import LocateResources
from pytrek.gui.gamepieces.GamePiece import GamePiece


class KlingonTorpedoFollower(GamePiece):

    def __init__(self):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME,
                                                           bareFileName='KlingonTorpedoFollower-16.png')

        GamePiece.__init__(self, filename=fqFileName)

        self._uuid:      uuid4 = uuid4()            # My ID
        self._following: uuid4 = cast(uuid4, None)

    @property
    def uuid(self) -> uuid4:
        return self._uuid

    @property
    def following(self) -> uuid4:
        """
        """
        return self._following

    @following.setter
    def following(self, newValue: uuid4):
        """
        Args:
            newValue:
        """
        self._following = newValue

