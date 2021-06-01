
from typing import cast

from logging import Logger
from logging import getLogger

from pytrek.LocateResources import LocateResources

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion
from pytrek.model.Coordinates import Coordinates


class Commander(GamePiece, SmoothMotion):

    nextId: int = 0

    def __init__(self, coordinates: Coordinates, moveInterval: int):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='Commander.png')

        GamePiece.__init__(self, filename=fqFileName)
        SmoothMotion.__init__(self)

        self.currentPosition = coordinates

        self._moveInterval: int   = moveInterval
        self._power:        float = cast(float, None)

        self.logger: Logger = getLogger(__name__)
        self._id:    int     = Commander.nextId

        Commander.nextId += 1

        # Compute at creation;  Mediator will move the commander
        arcadeX, arcadeY = GamePiece.gamePositionToScreenPosition(coordinates)

        self.center_x = arcadeX
        self.center_y = arcadeY


    @property
    def id(self) -> int:
        return self._id

    @property
    def power(self) -> float:
        return self._power

    @power.setter
    def power(self, theNewValue: float):
        self._power = theNewValue
