
from logging import Logger
from logging import getLogger
from typing import cast

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS
from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.Klingon import Klingon

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.Singleton import Singleton


class QuadrantMediator(Singleton):

    def init(self):

        self.logger: Logger = getLogger(__name__)

    def update(self, quadrant: Quadrant):

        self.logger.debug(f'{quadrant.enterpriseCoordinates=}')
        if quadrant.klingonCount > 0:
            self.logger.info(f'{quadrant.klingonCount=}')

        for y in range(QUADRANT_ROWS):
            for x in range(QUADRANT_COLUMNS):

                sector: Sector = quadrant.getSector(Coordinates(x, y))
                self.logger.debug(f'{sector}')

                gamePiece:  GamePiece  = sector.sprite
                sectorType: SectorType = sector.type

                if sectorType != SectorType.EMPTY:
                    if sectorType == SectorType.ENTERPRISE:
                        self._updateEnterprise(quadrant=quadrant, gamePiece=gamePiece)
                    elif sectorType == SectorType.KLINGON:
                        self._updateKlingon(quadrant=quadrant, gamePiece=gamePiece)

    def _updateEnterprise(self, quadrant: Quadrant, gamePiece: GamePiece):
        """
        Updates the Enterprise.  Account for in motion or stationary

        Args:
            quadrant:  The inspected quadrant
            gamePiece: The game piece found in the quadrant
        """
        enterprise: Enterprise = cast(Enterprise, gamePiece)
        arcadeX, arcadeY = GamePiece.gamePositionToScreenPosition(quadrant.enterpriseCoordinates)
        if enterprise.inMotion is True:

            self.logger.debug(f'Enterprise arcade position: ({arcadeX},{arcadeY})')
            enterprise.destinationPoint = ArcadePosition(x=arcadeX, y=arcadeY)
            enterprise.update()
        else:
            enterprise.center_x = arcadeX
            enterprise.center_y = arcadeY

    def _updateKlingon(self, quadrant: Quadrant, gamePiece: GamePiece):

        klingon: Klingon = cast(Klingon, gamePiece)

        arcadeX, arcadeY = GamePiece.gamePositionToScreenPosition(klingon.currentPosition)

        klingon.center_x = arcadeX
        klingon.center_y = arcadeY
