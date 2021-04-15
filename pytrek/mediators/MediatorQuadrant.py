
from logging import Logger
from logging import getLogger
from typing import cast

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS
from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.Singleton import Singleton


class MediatorQuadrant(Singleton):

    def init(self):

        self.logger: Logger = getLogger(__name__)

    def update(self, quadrant: Quadrant):

        self.logger.debug(f'{quadrant.enterpriseCoordinates=}')
        for y in range(QUADRANT_ROWS):
            for x in range(QUADRANT_COLUMNS):
                sector: Sector = quadrant.getSector(Coordinates(x, y))
                self.logger.debug(f'{sector}')
                gamePiece:  GamePiece  = sector.sprite
                sectorType: SectorType = sector.type

                if sectorType != SectorType.EMPTY:
                    if sectorType == SectorType.ENTERPRISE:
                        enterprise: Enterprise = cast(Enterprise, gamePiece)

                        arcadeX, arcadeY = GamePiece.gamePositionToScreenPosition(quadrant.enterpriseCoordinates)
                        if enterprise.inMotion is True:

                            self.logger.debug(f'Enterprise arcade position: ({arcadeX},{arcadeY})')
                            enterprise.destinationPoint = ArcadePosition(x=arcadeX, y=arcadeY)
                            enterprise.update()
                        else:
                            enterprise.center_x = arcadeX
                            enterprise.center_y = arcadeY

