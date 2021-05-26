from typing import List
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

from arcade import SpriteList
from arcade import Texture
from arcade import load_texture

from pytrek.Constants import QUADRANT_COLUMNS
from pytrek.Constants import QUADRANT_ROWS
from pytrek.LocateResources import LocateResources

from pytrek.engine.Computer import Computer
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.GameEngine import GameEngine

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.ExplosionColor import ExplosionColor
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.Klingon import Klingon

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

        self._playerList:    SpriteList = SpriteList()
        self._klingonList:   SpriteList = SpriteList()
        self._commanderList: SpriteList = SpriteList()

        self._klingonTorpedoes: SpriteList = SpriteList()
        self._torpedoFollowers: SpriteList = SpriteList(is_static=True)
        self._photonTorpedoes:  SpriteList = SpriteList()

        self._ktm.klingonTorpedoes = self._klingonTorpedoes
        self._ktm.torpedoFollowers = self._torpedoFollowers
        self._ptm.torpedoes        = self._photonTorpedoes

        self._photonTorpedoExplosions: List[Texture] = self._loadPhotonTorpedoExplosions()

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
        self._ptm.fireEnterpriseTorpedoesAtKlingons(enterprise=quadrant.enterprise, klingons=quadrant.klingons)

    def draw(self, quadrant: Quadrant):
        self.playerList.draw()
        self.klingonList.draw()
        self._klingonTorpedoes.draw()
        self._torpedoFollowers.draw()
        if quadrant.hasPlanet is True:
            quadrant._planet.draw()

        self._ptm.draw(quadrant=quadrant)

    def update(self, quadrant: Quadrant):

        if self.logger.getEffectiveLevel() == DEBUG:
            self.logger.debug(f'{quadrant.enterpriseCoordinates=}')
            if quadrant.klingonCount > 0:
                self.logger.debug(f'{quadrant.klingonCount=}')

        self._updateQuadrant(quadrant)

        self._ktm.fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant)
        self.playerList.update()
        self._klingonTorpedoes.update()
        self._torpedoFollowers.update()

        self._ktm.handleKlingonTorpedoHits(quadrant)
        self._ktm.handleKlingonTorpedoMisses()

        self._ptm.update(quadrant=quadrant)
        self._ptm.handleTorpedoHits(quadrant=quadrant)

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

    def _loadPhotonTorpedoExplosions(self) -> List[Texture]:
        """
        Cache the torpedo explosion textures

        Returns:  The list
        """
        explosions: List[Texture] = []

        for eColor in ExplosionColor:
            bareFileName: str = f'explosion_rays_{eColor.value}.png'
            fqFileName:   str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=bareFileName)

            explosion = load_texture(fqFileName)
            explosions.append(explosion)

        return explosions
