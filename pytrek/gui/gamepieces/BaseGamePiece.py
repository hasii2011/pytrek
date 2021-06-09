
from typing import cast

from arcade import Sprite

from pytrek.LocateResources import LocateResources

from pytrek.model.Coordinates import Coordinates


class BaseGamePiece(Sprite):

    def __init__(self, filename: str = None, scale: float = 1.0):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=filename)

        super().__init__(filename=fqFileName, scale=scale)

        self._gameCoordinates: Coordinates = cast(Coordinates, None)

    @property
    def gameCoordinates(self) -> Coordinates:
        """

        Returns:  The current quadrant position
        """
        return self._gameCoordinates

    @gameCoordinates.setter
    def gameCoordinates(self, newValue: Coordinates):
        self._gameCoordinates = newValue
