
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion

from pytrek.LocateResources import LocateResources

from pytrek.model.Coordinates import Coordinates

CommanderId = NewType('CommanderId', str)


class Commander(GamePiece, SmoothMotion):

    def __init__(self, coordinates: Coordinates, moveInterval: int):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='Commander.png')

        GamePiece.__init__(self, filename=fqFileName)
        SmoothMotion.__init__(self)

        self.logger: Logger = getLogger(__name__)

        self.gameCoordinates = coordinates

        self._moveInterval: int   = moveInterval

        self._timeSinceMovement: float = cast(float, None)
        self._power:             float = cast(float, None)

        self._id: CommanderId     = CommanderId(f'Commander-{self.gameCoordinates}')

        # Compute at creation;  Mediator will move the commander
        arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(coordinates)

        self.center_x = arcadePoint.x
        self.center_y = arcadePoint.y

    @property
    def id(self) -> CommanderId:
        return self._id

    @property
    def power(self) -> float:
        return self._power

    @power.setter
    def power(self, theNewValue: float):
        self._power = theNewValue

    @property
    def timeSinceMovement(self) -> float:
        return self._timeSinceMovement

    @timeSinceMovement.setter
    def timeSinceMovement(self, newValue: float):
        self._timeSinceMovement = newValue

    @property
    def moveInterval(self) -> int:
        return self._moveInterval

    @moveInterval.setter
    def moveInterval(self, newValue: int):
        self._moveInterval = newValue

    def __str__(self):

        lookAtMe: str = (
            f'Commander['
            f'id={self.id} '
            f'power={self.power:.3f} '
            f'moveInterval={self.moveInterval} '
            f'timeSinceMovement={self.timeSinceMovement} '
            f'currentPosition={self.gameCoordinates}'
            ']'
        )
        return lookAtMe

    def __repr__(self):
        return self.__str__()
