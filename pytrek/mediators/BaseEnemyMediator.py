
from typing import cast

from logging import Logger
from logging import getLogger

from random import choice as randomChoice

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Direction import Direction

from pytrek.gui.gamepieces.base.BaseEnemy import BaseEnemy
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.mediators.BaseMediator import BaseMediator


class BaseEnemyMediator(BaseMediator):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):
        super().__init__()

    def _enemyMovedUpdateQuadrant(self, quadrant: Quadrant, enemy: BaseEnemy, newSectorCoordinates: Coordinates, oldSectorCoordinates: Coordinates):
        """

        Args:
            quadrant:  Quadrant to modify
            enemy:     sprite to place in sector
            newSectorCoordinates:    old sector coordinates
            oldSectorCoordinates:    new sector coordinates

        """
        self.logger: Logger = BaseEnemyMediator.clsLogger

        oldSector: Sector = quadrant.getSector(sectorCoordinates=oldSectorCoordinates)

        oldSector.type   = SectorType.EMPTY
        oldSector.sprite = cast(GamePiece, None)

        newSector: Sector = quadrant.getSector(sectorCoordinates=newSectorCoordinates)

        newSector.type   = SectorType.COMMANDER
        newSector.sprite = enemy

    def _evade(self, currentLocation: Coordinates) -> Coordinates:
        """
        Move commander around to avoid torpedoes

        Args:
            currentLocation:

        Returns:  New random coordinates
        """
        while True:
            pDirection:     Direction   = self.__randomDirection_()
            newCoordinates: Coordinates = currentLocation.newCoordinates(pDirection)

            self.logger.debug(f"Random direction {pDirection.name}: currentLocation: {currentLocation} newCoordinates {newCoordinates}")
            if newCoordinates.valid():
                break
        return newCoordinates

    def _toArcadePoint(self, enemy: BaseEnemy, newPosition: Coordinates):
        """
        Sets the arcade points for the input enemy.
        Args:
            enemy:   The enemy that moved
            newPosition: Its' new game position

        """
        arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(newPosition)
        enemy.center_x = arcadePoint.x
        enemy.center_y = arcadePoint.y

    def __randomDirection_(self) -> Direction:
        """

        Returns:  A random direction
        """
        return randomChoice(list(Direction))
