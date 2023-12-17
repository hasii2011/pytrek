
from typing import cast

from logging import Logger
from logging import getLogger

from codeallybasic.Singleton import Singleton

from pytrek.GameState import GameState

from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine

from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType


class GalaxyMediator(Singleton):
    """
    This class aids in updating the Galaxy model and the game state
    """
    # noinspection PyAttributeOutsideInit
    def init(self, *args, **kwargs):

        self.logger: Logger = getLogger(__name__)

        self._computer:   Computer   = Computer()
        self._gameState:  GameState  = GameState()
        self._gameEngine: GameEngine = GameEngine()
        self._galaxy:     Galaxy     = Galaxy()

    def doWarp(self, currentCoordinates: Coordinates, destinationCoordinates: Coordinates, warpSpeed: float):
        """
        This actually moves the Enterprise and updates the Game State

        Args:
            currentCoordinates:     Where we were
            destinationCoordinates: Where we want to go
            warpSpeed:              How fast we want to go
        """

        travelDistance: float = self._computer.computeGalacticDistance(startQuadrantCoordinates=currentCoordinates,
                                                                       endQuadrantCoordinates=destinationCoordinates)
        energyConsumed: float = self._gameEngine.computeEnergyForWarpTravel(travelDistance=travelDistance, warpFactor=warpSpeed)

        self._gameState.energy -= energyConsumed
        self._gameEngine.updateTimeAfterWarpTravel(travelDistance=travelDistance, warpFactor=warpSpeed)

        self.logger.info(f'After warp travel consumed energy: {energyConsumed:.2f}')

        currentQuadrant: Quadrant = self._galaxy.getQuadrant(quadrantCoordinates=currentCoordinates)

        sectorCoordinates: Coordinates = currentQuadrant.enterpriseCoordinates
        oldSector:         Sector      = currentQuadrant.getSector(sectorCoordinates=sectorCoordinates)

        oldSector.type   = SectorType.EMPTY
        oldSector.sprite = cast(GamePiece, None)
        #
        # Set up new quadrant
        #
        destinationQuadrant                         = self._galaxy.getQuadrant(quadrantCoordinates=destinationCoordinates)
        self._galaxy.currentQuadrant                = destinationQuadrant
        self._gameState.currentQuadrantCoordinates = self._galaxy.currentQuadrant.coordinates
