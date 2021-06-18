
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import SpriteList

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.mediators.BaseMediator import BaseMediator
from pytrek.mediators.BaseMediator import LineOfSightResponse

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType


class EnterpriseMediator(BaseMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._soundImpulse:        Sound = cast(Sound, None)
        self._soundUnableToComply: Sound = cast(Sound, None)
        self._soundRepeatRequest:  Sound = cast(Sound, None)

        self._loadSounds()

    def update(self, quadrant: Quadrant):

        enterprise: Enterprise = quadrant.enterprise

        arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(quadrant.enterpriseCoordinates)
        arcadeX:     float       = arcadePoint.x
        arcadeY:     float       = arcadePoint.y
        if enterprise.inMotion is True:

            self.logger.debug(f'Enterprise arcade position: ({arcadeX},{arcadeY})')
            enterprise.destinationPoint = ArcadePoint(x=arcadeX, y=arcadeY)
            enterprise.update()
        else:
            enterprise.center_x = arcadeX
            enterprise.center_y = arcadeY

    def impulse(self, quadrant: Quadrant, arcadePoint: ArcadePoint):

        targetCoordinates:     Coordinates = self._computer.computeSectorCoordinates(x=arcadePoint.x, y=arcadePoint.y)
        enterpriseCoordinates: Coordinates = self._gameState.currentSectorCoordinates
        soundVolume:           float      = self._gameSettings.soundVolume.value

        if targetCoordinates == enterpriseCoordinates:
            self._messageConsole.displayMessage("WTF.  You are already here!")
            self._soundUnableToComply.play(volume=soundVolume)
        else:
            startingPoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(enterpriseCoordinates)
            endPoint:      ArcadePoint = arcadePoint

            results: LineOfSightResponse = self._doWeHaveLineOfSight(quadrant=quadrant, startingPoint=startingPoint, endPoint=endPoint)
            if results.answer is True:
                self.__updateQuadrant(quadrant=quadrant, currentCoordinates=enterpriseCoordinates, targetCoordinates=targetCoordinates)
                quadrant.enterprise.inMotion    = True
                quadrant.enterpriseCoordinates = targetCoordinates
                self._gameEngine.impulse(newCoordinates=targetCoordinates, quadrant=quadrant, enterprise=quadrant.enterprise)
                self._soundImpulse.play(volume=soundVolume)
            else:
                self._messageConsole.displayMessage(f'Destination is blocked by: {results.obstacle.id}')
                self._soundRepeatRequest.play(volume=soundVolume)

                stopEnergy: float = self._gameEngine.computeEnergyWhenBlocked(startSector=enterpriseCoordinates, endSector=targetCoordinates)
                self._gameState.energy -= stopEnergy
                #
                # TODO move Enterprise "Close" to where it was 'blocked'

        # StarTrekScreen.quitIfTimeExpired()
        # self._dockIfAdjacentToStarbase()

    def warp(self):
        pass

    def _loadSounds(self):

        self._soundImpulse        = self._loadSound(bareFileName='impulse.wav')
        self._soundUnableToComply = self._loadSound(bareFileName='unableToComply.wav')
        self._soundRepeatRequest  = self._loadSound(bareFileName='pleaseRepeatRequest.wav')

    def _doWeHaveLineOfSight(self, quadrant: Quadrant, startingPoint: ArcadePoint, endPoint: ArcadePoint) -> LineOfSightResponse:
        """
        Check to see if planets, stars, other Klingons, Commanders, or StarBases prevent
        the Enterprise from traveling to the selected sector

        Args:
            startingPoint:

        Returns:  `True` if no obstructions, else `False`
        """
        obstacles: SpriteList = SpriteList()
        if quadrant.hasPlanet is True:
            obstacles.append(quadrant._planet)
        obstacles.extend(quadrant.klingons)
        obstacles.extend(quadrant.commanders)
        results: LineOfSightResponse = self._hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.info(f'{results=}')
        return results

    def __updateQuadrant(self, quadrant: Quadrant, currentCoordinates: Coordinates, targetCoordinates: Coordinates) -> Quadrant:
        """

        Args:
            quadrant:           What we are updating
            currentCoordinates: Where we are
            targetCoordinates:  Where we are going

        Returns: The updated input quadrant
        """

        currentSector: Sector = quadrant.getSector(currentCoordinates)
        targetSector:  Sector = quadrant.getSector(targetCoordinates)

        currentSector.type = SectorType.EMPTY
        targetSector.type  = SectorType.ENTERPRISE

        return quadrant