
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from src.pytrek.engine.ArcadePoint import ArcadePoint
from src.pytrek.engine.GameEngine import GameEngine
from src.pytrek.engine.Intelligence import Intelligence

from src.pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo

from src.pytrek.gui.gamepieces.base.BaseMiss import BaseMiss
from src.pytrek.gui.gamepieces.GamePiece import GamePiece
from src.pytrek.gui.gamepieces.SmoothMotion import SmoothMotion

from src.pytrek.gui.gamepieces.klingon.KlingonTorpedo import KlingonTorpedo
from src.pytrek.gui.gamepieces.klingon.KlingonTorpedoMiss import KlingonTorpedoMiss
from src.pytrek.gui.MessageConsoleProxy import MessageConsoleProxy

from src.pytrek.model.Coordinates import Coordinates
from src.pytrek.model.Quadrant import Quadrant
from src.pytrek.model.Sector import Sector
from src.pytrek.model.SectorType import SectorType

from src.pytrek.settings.GameSettings import GameSettings

from src.pytrek.GameState import GameState

from src.pytrek.mediators.base.BaseMediator import BaseMediator

Torpedoes            = List[SmoothMotion]
Misses               = List[BaseMiss]


class MissesMediator(BaseMediator):

    """
    Has common stuff to handle torpedo misses
    """
    def __init__(self):

        self._missesMediatorLogger: Logger = getLogger(__name__)

        super().__init__()

        self._gameState:      GameState    = GameState()
        self._gameEngine:     GameEngine   = GameEngine()
        self._intelligence:   Intelligence = Intelligence()
        self._gameSettings:   GameSettings = GameSettings()

        assert MessageConsoleProxy().initialized is True, 'Console proxy needs to be already initialized'
        self._messageConsole: MessageConsoleProxy = MessageConsoleProxy()

    def _findTorpedoMisses(self, torpedoes: Torpedoes) -> List[BaseEnemyTorpedo]:

        torpedoDuds: List[BaseEnemyTorpedo] = []
        for smoothMotion in torpedoes:
            torpedo: KlingonTorpedo = cast(KlingonTorpedo, smoothMotion)
            if torpedo.inMotion is False:
                torpedoDuds.append(torpedo)
        return torpedoDuds

    def _handleMissRemoval(self, quadrant: Quadrant, misses: Misses):

        currentTime:     float = self._gameEngine.gameClock
        displayInterval: int   = self._gameSettings.basicMissDisplayInterval

        for miss in misses:
            dud: BaseMiss = cast(BaseMiss, miss)
            deltaTime: float = currentTime - dud.placedTime
            if deltaTime >= displayInterval:
                gameCoordinates: Coordinates = dud.gameCoordinates
                self.__removeMissInQuadrant(quadrant=quadrant, sectorCoordinates=gameCoordinates)
                dud.remove_from_sprite_lists()

    def _placeMiss(self, quadrant: Quadrant, torpedoDud: GamePiece, miss: BaseMiss):
        """
        Convert to game coordinates
        Then to game point in order to get miss center as a sector coordinates

        Args:
            miss:  The appropriate "miss" sprite
        """

        gameCoordinates: Coordinates = self._computer.computeSectorCoordinates(x=torpedoDud.center_x, y=torpedoDud.center_y)
        arcadePoint:     ArcadePoint = GamePiece.gamePositionToScreenPosition(gameCoordinates=gameCoordinates)

        miss.center_x = arcadePoint.x
        miss.center_y = arcadePoint.y

        if isinstance(miss, KlingonTorpedoMiss):
            sectorType: SectorType = SectorType.KLINGON_TORPEDO_MISS
        else:
            sectorType = SectorType.ENTERPRISE_TORPEDO_MISS

        miss.gameCoordinates = gameCoordinates
        self.__placeMissInQuadrant(quadrant, gameCoordinates, sectorType)
        self._missesMediatorLogger.info(f'Placed miss at: {gameCoordinates=}  {arcadePoint=}')

    def __placeMissInQuadrant(self, quadrant: Quadrant, sectorCoordinates: Coordinates, sectorType: SectorType):

        sector: Sector = quadrant.getSector(sectorCoordinates)

        sector.type = sectorType

    def __removeMissInQuadrant(self, quadrant: Quadrant, sectorCoordinates: Coordinates):

        sector: Sector = quadrant.getSector(sectorCoordinates)

        sector.type = SectorType.EMPTY
