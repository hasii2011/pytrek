
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

from arcade import MOUSE_BUTTON_RIGHT
from arcade import SpriteList

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS

from pytrek.engine.Computer import Computer
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.GameEngine import GameEngine

from pytrek.gui.gamepieces.Commander import Commander

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.mediators.CommanderMediator import CommanderMediator

from pytrek.mediators.EnterpriseMediator import EnterpriseMediator
from pytrek.mediators.KlingonTorpedoMediator import KlingonTorpedoMediator
from pytrek.mediators.PhotonTorpedoMediator import PhotonTorpedoMediator

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

        self._ktm: KlingonTorpedoMediator = KlingonTorpedoMediator()
        self._ptm: PhotonTorpedoMediator  = PhotonTorpedoMediator()
        self._em:  EnterpriseMediator     = EnterpriseMediator()
        self._cm:  CommanderMediator      = CommanderMediator()

        self._playerList:    SpriteList = SpriteList()
        self._klingonList:   SpriteList = SpriteList()
        self._commanderList: SpriteList = SpriteList()

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
        self._ktm.klingonList = newValues

    @property
    def commanderList(self) -> SpriteList:
        return self._commanderList

    @commanderList.setter
    def commanderList(self, newValues: SpriteList):
        self._commanderList = newValues

    def fireEnterpriseTorpedoesAtKlingons(self, quadrant: Quadrant):
        self._ptm.fireEnterpriseTorpedoesAtKlingons(quadrant=quadrant)

    # noinspection PyUnusedLocal
    def handleMousePress(self, quadrant: Quadrant, arcadePoint: ArcadePoint, button: int, keyModifiers: int):

        if button == MOUSE_BUTTON_RIGHT:
            self._em.impulse(quadrant=quadrant, arcadePoint=arcadePoint)

    def draw(self, quadrant: Quadrant):
        self.playerList.draw()
        self.klingonList.draw()
        self.commanderList.draw()
        self._ktm.draw()
        if quadrant.hasPlanet is True:
            quadrant._planet.draw()

        self._ptm.draw(quadrant=quadrant)

    def update(self, quadrant: Quadrant):

        if self.logger.getEffectiveLevel() == DEBUG:
            self.logger.debug(f'{quadrant.enterpriseCoordinates=}')
            if quadrant.klingonCount > 0:
                self.logger.debug(f'{quadrant.klingonCount=}')

        self._updateQuadrant(quadrant)
        self.playerList.update()

        self._ktm.update(quadrant=quadrant)

        self._ptm.update(quadrant=quadrant)

    def _updateQuadrant(self, quadrant):
        for y in range(QUADRANT_ROWS):
            for x in range(QUADRANT_COLUMNS):

                sector: Sector = quadrant.getSector(Coordinates(x, y))
                self.logger.debug(f'{sector}')

                gamePiece: GamePiece = sector.sprite
                sectorType: SectorType = sector.type

                if sectorType != SectorType.EMPTY:
                    if sectorType == SectorType.ENTERPRISE:
                        # self._updateEnterprise(quadrant=quadrant, gamePiece=gamePiece)
                        self._em.update(quadrant=quadrant)
                    elif sectorType == SectorType.KLINGON:
                        self._updateKlingon(gamePiece=gamePiece)
                    elif sectorType == SectorType.PLANET:
                        pass
                        # Planets are immovable;  So arcade position set at creation
                    elif sectorType == SectorType.COMMANDER:
                        # self._updateCommander(quadrant=quadrant, commander=cast(Commander, gamePiece))
                        self._cm.update(quadrant=quadrant, commander=cast(Commander, gamePiece))
                    else:
                        assert False, 'Bad Game Piece'

    def _updateKlingon(self, gamePiece: GamePiece):

        klingon: Klingon = cast(Klingon, gamePiece)

        arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(klingon.currentPosition)

        klingon.center_x = arcadePoint.x
        klingon.center_y = arcadePoint.y
