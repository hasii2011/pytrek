
from typing import cast

from logging import Logger
from logging import getLogger

from random import choice as randomChoice

from arcade import Sound

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Direction import Direction

from pytrek.gui.gamepieces.Commander import Commander
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType

from pytrek.mediators.BaseEnemyMediator import BaseEnemyMediator


class CommanderMediator(BaseEnemyMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._commanderMove: Sound = cast(Sound, None)

        self._loadSounds()

    def update(self, quadrant: Quadrant, commander: Commander):

        currentTime:    float = self._gameEngine.gameClock
        deltaClockTime: float = currentTime - commander.timeSinceMovement
        if deltaClockTime > commander.moveInterval:

            oldPosition: Coordinates = commander.gameCoordinates
            newPosition: Coordinates = self.evade(currentLocation=oldPosition)
            while True:
                if self._checkCommanderMoveIsValid(quadrant=quadrant, targetCoordinates=newPosition):
                    break
                else:
                    newPosition: Coordinates = self.evade(currentLocation=oldPosition)

            self.logger.info(f'Commander moves from {oldPosition} to {newPosition}')
            self._enemyMovedUpdateQuadrant(quadrant=quadrant, enemy=commander, newPosition=newPosition, oldPosition=oldPosition)
            self._commanderMove.play(self._gameSettings.soundVolume.value)

            commander.gameCoordinates = newPosition

            arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(newPosition)

            commander.center_x = arcadePoint.x
            commander.center_y = arcadePoint.y

            commander.timeSinceMovement = currentTime

    def evade(self, currentLocation: Coordinates) -> Coordinates:
        """
        Move commander around to avoid torpedoes

        Args:
            currentLocation:

        Returns:  New random coordinates
        """
        while True:
            pDirection:     Direction   = self._randomDirection_()
            newCoordinates: Coordinates = currentLocation.newCoordinates(pDirection)

            self.logger.debug(f"Random direction {pDirection.name}: currentLocation: {currentLocation} newCoordinates {newCoordinates}")
            if newCoordinates.valid():
                break
        return newCoordinates

    def _randomDirection_(self) -> Direction:
        """

        Returns:  A random direction
        """
        return randomChoice(list(Direction))

    def _checkCommanderMoveIsValid(self, quadrant: Quadrant, targetCoordinates: Coordinates) -> bool:

        targetSector: Sector = quadrant.getSector(targetCoordinates)
        if targetSector.type == SectorType.EMPTY:
            return True
        else:
            self.logger.info(f'Commander cannot move to sector: {targetCoordinates} occupied by {targetSector.type}')
            return False

    def _loadSounds(self):

        self._commanderMove = self._loadSound(bareFileName='CommanderMove.wav')
