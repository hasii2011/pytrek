from logging import Logger
from logging import getLogger

from arcade import Sprite

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.PlanetType import PlanetType

from pytrek.LocateResources import LocateResources
from pytrek.model.Coordinates import Coordinates


class Planet(Sprite):

    def __init__(self, planetType: PlanetType, sectorCoordinates: Coordinates):

        self.logger: Logger = getLogger(__name__)

        bareFileName: str = f'{planetType.value}.png'
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=f'{bareFileName}')

        super().__init__(filename=fqFileName, scale=0.35)

        # Compute these once since planets don't move
        arcadeX, arcadeY = GamePiece.gamePositionToScreenPosition(sectorCoordinates)

        self.center_x = arcadeX
        self.center_y = arcadeY

        self._type: PlanetType = planetType
        self._id:   str        = f'{self._type.value} type planet'

    @property
    def id(self) -> str:
        return self._id
