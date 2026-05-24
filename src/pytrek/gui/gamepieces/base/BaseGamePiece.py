
from typing import cast

from arcade import Sprite
from arcade import Texture
from arcade import load_texture

from pytrek.LocateResources import LocateResources

from pytrek.model.Coordinates import Coordinates


class BaseGamePiece(Sprite):

    def __init__(self, filename: str = '', scale: float = 1.0):

        fqFileName: str = LocateResources.getImagePath(bareFileName=filename)

        texture: Texture = load_texture(fqFileName)
        super().__init__(texture, scale=scale)

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
