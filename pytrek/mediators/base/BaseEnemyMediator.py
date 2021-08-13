
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

from pytrek.mediators.base.MissesMediator import MissesMediator


class BaseEnemyMediator(MissesMediator):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):
        super().__init__()

    def _playMoveSound(self):
        """
        Must be implemented by subclass or you will hear nada' if enemy moves
        """
        pass

    def moveEnemy(self, quadrant: Quadrant, enemy: BaseEnemy):

        currentTime:    float = self._gameEngine.gameClock
        deltaClockTime: float = currentTime - enemy.timeSinceMovement
        if deltaClockTime > enemy.moveInterval:

            oldPosition: Coordinates = enemy.gameCoordinates
            newPosition: Coordinates = self._keepTryingToMoveUntilValid(quadrant, oldPosition)

            self.logger.info(f'Enemy {enemy} moves from {oldPosition} to {newPosition}')
            self._enemyMovedUpdateQuadrant(quadrant=quadrant, enemy=enemy, newSectorCoordinates=newPosition, oldSectorCoordinates=oldPosition)

            enemy.gameCoordinates = newPosition
            self._toArcadePoint(enemy, newPosition)
            enemy.timeSinceMovement = currentTime

            self._playMoveSound()

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

    def _keepTryingToMoveUntilValid(self, quadrant: Quadrant, oldPosition: Coordinates):

        newPosition: Coordinates = self._evade(currentLocation=oldPosition)

        while True:
            if self._checkEnemyMoveIsValid(quadrant=quadrant, targetCoordinates=newPosition):
                break
            else:
                newPosition = self._evade(currentLocation=oldPosition)
        return newPosition

    def _checkEnemyMoveIsValid(self, quadrant: Quadrant, targetCoordinates: Coordinates) -> bool:

        targetSector: Sector = quadrant.getSector(targetCoordinates)
        if targetSector.type == SectorType.EMPTY:
            return True
        else:
            self.logger.info(f'Commander cannot move to sector: {targetCoordinates} occupied by {targetSector.type}')
            return False

    def _evade(self, currentLocation: Coordinates) -> Coordinates:
        """
        Move enemy around to avoid torpedoes

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
