
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

from arcade import SpriteList

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS

from pytrek.engine.Computer import Computer
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.GameEngine import GameEngine

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.Klingon import Klingon

from pytrek.mediators.KlingonTorpedoHandler import KlingonTorpedoHandler

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.Singleton import Singleton


class QuadrantMediator(Singleton):
    """
    This class avoids putting UI logic (arcade) in the model class, Quadrant.
    """

    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        self._gameEngine: GameEngine = GameEngine()
        self._computer:   Computer   = Computer()

        self._kth: KlingonTorpedoHandler = KlingonTorpedoHandler()

        self._playerList:    SpriteList = SpriteList()
        self._klingonList:   SpriteList = SpriteList()
        self._commanderList: SpriteList = SpriteList()

        self._klingonTorpedoes: SpriteList = cast(SpriteList, None)
        self._torpedoFollowers: SpriteList = cast(SpriteList, None)

    @property
    def playerList(self) -> SpriteList:
        return self._playerList

    @playerList.setter
    def playerList(self, newValues: SpriteList):
        self._playerList = newValues

    @property
    def klingonList(self) -> SpriteList:
        return self._klingonList

    @klingonList.setter
    def klingonList(self, newValues: SpriteList):
        self._klingonList     = newValues
        self._kth.klingonList = newValues

    @property
    def commanderList(self) -> SpriteList:
        return self._commanderList

    @commanderList.setter
    def commanderList(self, newValues: SpriteList):
        self._commanderList = newValues

    @property
    def klingonTorpedoes(self) -> SpriteList:
        return self._klingonTorpedoes

    @klingonTorpedoes.setter
    def klingonTorpedoes(self, newList: SpriteList):
        """
        Args:
            newList:
        """
        self._klingonTorpedoes = newList
        self._kth.klingonTorpedoes = newList

    @property
    def torpedoFollowers(self) -> SpriteList:
        return self._torpedoFollowers

    @torpedoFollowers.setter
    def torpedoFollowers(self, newList: SpriteList):
        self._torpedoFollowers = newList
        self._kth.torpedoFollowers = newList

    def draw(self, quadrant: Quadrant):
        self.playerList.draw()
        self.klingonList.draw()
        self.klingonTorpedoes.draw()
        self.torpedoFollowers.draw()
        if quadrant.hasPlanet is True:
            quadrant._planet.draw()

    def update(self, quadrant: Quadrant):

        if self.logger.getEffectiveLevel() == DEBUG:
            self.logger.debug(f'{quadrant.enterpriseCoordinates=}')
            if quadrant.klingonCount > 0:
                self.logger.debug(f'{quadrant.klingonCount=}')

        self._updateQuadrant(quadrant)

        self._kth.fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant)
        self.playerList.update()
        self.klingonTorpedoes.update()
        self.torpedoFollowers.update()

        self._kth.handleKlingonTorpedoHits(quadrant)
        self._kth.handleKlingonTorpedoMisses()

    def _updateQuadrant(self, quadrant):
        for y in range(QUADRANT_ROWS):
            for x in range(QUADRANT_COLUMNS):

                sector: Sector = quadrant.getSector(Coordinates(x, y))
                self.logger.debug(f'{sector}')

                gamePiece: GamePiece = sector.sprite
                sectorType: SectorType = sector.type

                if sectorType != SectorType.EMPTY:
                    if sectorType == SectorType.ENTERPRISE:
                        self._updateEnterprise(quadrant=quadrant, gamePiece=gamePiece)
                    elif sectorType == SectorType.KLINGON:
                        self._updateKlingon(gamePiece=gamePiece)
                    elif sectorType == SectorType.PLANET:
                        pass
                        # Planets are immovable;  So arcade position set at creation

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
            enterprise.destinationPoint = ArcadePoint(x=arcadeX, y=arcadeY)
            enterprise.update()
        else:
            enterprise.center_x = arcadeX
            enterprise.center_y = arcadeY

    def _updateKlingon(self, gamePiece: GamePiece):

        klingon: Klingon = cast(Klingon, gamePiece)

        arcadeX, arcadeY = GamePiece.gamePositionToScreenPosition(klingon.currentPosition)

        klingon.center_x = arcadeX
        klingon.center_y = arcadeY
