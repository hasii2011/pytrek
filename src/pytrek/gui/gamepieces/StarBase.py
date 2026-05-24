from logging import Logger
from logging import getLogger

from pytrek.gui.gamepieces.base.BaseGamePiece import BaseGamePiece

from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.model.Coordinates import Coordinates


class StarBase(BaseGamePiece):

    FILENAME: str = "StarBase.png"

    nextId: int = 0

    def __init__(self, sectorCoordinates: Coordinates):

        self.logger: Logger = getLogger(__name__)

        super().__init__(filename=StarBase.FILENAME, scale=0.25)

        # Compute these once since StarBase's don't move
        self.gameCoordinates     = sectorCoordinates
        arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(sectorCoordinates)

        self.center_x = arcadePoint.x
        self.center_y = arcadePoint.y

        self._id: str = f'StarBase-{StarBase.nextId}'

        StarBase.nextId += 1

    @property
    def id(self) -> str:
        return self._id

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return self.__str__()
