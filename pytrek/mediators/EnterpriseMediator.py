
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import SpriteList
# from arcade import View

from arcade import schedule
from arcade import unschedule

from pytrek.Constants import MAX_QUADRANT_X_COORDINATE
from pytrek.Constants import MAX_QUADRANT_Y_COORDINATE
from pytrek.Constants import MAX_SECTOR_X_COORDINATE
from pytrek.Constants import MAX_SECTOR_Y_COORDINATE
from pytrek.Constants import MIN_QUADRANT_X_COORDINATE
from pytrek.Constants import MIN_QUADRANT_Y_COORDINATE
from pytrek.Constants import MIN_SECTOR_X_COORDINATE
from pytrek.Constants import MIN_SECTOR_Y_COORDINATE

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType

from pytrek.commandparser.InvalidCommandValueException import InvalidCommandValueException

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.DirectionData import DirectionData
from pytrek.engine.ShipCondition import ShipCondition

from pytrek.gui.UITypes import WarpTravelCallbackV2

from pytrek.gui.WarpEffectSection import WarpEffectSection

from pytrek.mediators.base.MissesMediator import MissesMediator
from pytrek.mediators.base.BaseMediator import LineOfSightResponse

from pytrek.gui.gamepieces.base.BaseGamePiece import BaseGamePiece
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant
from pytrek.model.Sector import Sector
from pytrek.model.SectorType import SectorType


class EnterpriseMediator(MissesMediator):
    """
    This is not a singleton.
    It requires 2 properties to be injected at appropriate times
    """

    def __init__(self):
        """
        """
        super().__init__()

        self._warpTravelCallback: WarpTravelCallbackV2 = cast(WarpTravelCallbackV2, None)
        self._warpEffectSection:  WarpEffectSection    = cast(WarpEffectSection,    None)

        self.logger:                  Logger       = getLogger(__name__)
        self._soundMachine:           SoundMachine = SoundMachine()
        self._warpSpeed:              float        = 0.0
        self._destinationCoordinates: Coordinates  = cast(Coordinates, None)
        """
        Use to store the warp coordinates use after the warp effect is compete
        """

    def _setWarpEffectSection(self, newValue: WarpEffectSection):
        self._warpEffectSection = newValue

    def _setWarpTravelCallback(self, newValue: WarpTravelCallbackV2):
        self._warpTravelCallback = newValue

    # noinspection PyTypeChecker
    warpEffectSection = property(fget=None,  fset=_setWarpEffectSection,  doc='Set by the section UI')
    # noinspection PyTypeChecker
    warpTravelCallback = property(fget=None, fset=_setWarpTravelCallback, doc='Set by the section UI')

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

    def doDeveloperImpulseMove(self, quadrant: Quadrant, arcadePoint: ArcadePoint):
        """
        TODO:   Make a debug option
        Keep this around for developer use;  So I can click on the board to move
        the Enterprise
        Args:
            quadrant:
            arcadePoint:
        """

        targetCoordinates:     Coordinates = self._computer.computeSectorCoordinates(x=arcadePoint.x, y=arcadePoint.y)
        enterpriseCoordinates: Coordinates = self._gameState.currentSectorCoordinates

        if targetCoordinates == enterpriseCoordinates:
            self._messageConsole.displayMessage("WTF.  You are already here!")
            self._soundMachine.playSound(SoundType.UnableToComply)
        else:
            startingPoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(enterpriseCoordinates)
            endPoint:      ArcadePoint = arcadePoint

            results: LineOfSightResponse = self._doWeHaveLineOfSight(quadrant=quadrant, startingPoint=startingPoint, endPoint=endPoint)
            if results.answer is True:
                self._doImpulseMove(quadrant=quadrant, enterpriseCoordinates=enterpriseCoordinates, targetCoordinates=targetCoordinates)
            else:
                self._doBlockedImpulseMove(quadrant=quadrant, enterpriseCoordinates=enterpriseCoordinates, results=results)

        # StarTrekScreen.quitIfTimeExpired()
        # self._dockIfAdjacentToStarBase()

    def manualMove(self, quadrant: Quadrant, deltaX: float, deltaY: float):

        # Impulse move ?
        if 0.0 < deltaX < 1.0:
            self._doManualImpulseMove(deltaX, deltaY, quadrant)
        else:
            self._doManualWarpMove(int(deltaX), int(deltaY))

    def automaticMove(self, quadrant: Quadrant, quadrantCoordinates: Coordinates, sectorCoordinates: Coordinates):
        pass

    def _doManualImpulseMove(self, deltaX, deltaY, quadrant):

        enterpriseSectorCoordinates: Coordinates = self._gameState.currentSectorCoordinates
        targetSector: Coordinates = Coordinates()
        targetSector.x = enterpriseSectorCoordinates.x + int(deltaX * 10)
        targetSector.y = enterpriseSectorCoordinates.y + int(deltaY * 10)
        self._validateCoordinates(coordinate=targetSector,
                                  minX=MIN_SECTOR_X_COORDINATE,
                                  maxX=MAX_SECTOR_X_COORDINATE,
                                  minY=MIN_SECTOR_Y_COORDINATE,
                                  maxY=MAX_SECTOR_Y_COORDINATE)
        if targetSector == enterpriseSectorCoordinates:
            self._messageConsole.displayMessage("WTF.  You are already here!")
            self._soundMachine.playSound(SoundType.UnableToComply)
        else:
            arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(gameCoordinates=targetSector)
            startingPoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(enterpriseSectorCoordinates)
            endPoint: ArcadePoint = arcadePoint

            results: LineOfSightResponse = self._doWeHaveLineOfSight(quadrant=quadrant, startingPoint=startingPoint, endPoint=endPoint)
            if results.answer is True:
                self._doImpulseMove(quadrant=quadrant, enterpriseCoordinates=enterpriseSectorCoordinates, targetCoordinates=targetSector)
            else:
                self._doBlockedImpulseMove(quadrant=quadrant, enterpriseCoordinates=enterpriseSectorCoordinates, results=results)

    def _doManualWarpMove(self, deltaX: int, deltaY: int):

        enterpriseQuadrantCoordinates: Coordinates = self._gameState.currentQuadrantCoordinates
        targetQuadrantCoordinates:   Coordinates = Coordinates()
        targetQuadrantCoordinates.x = enterpriseQuadrantCoordinates.x + deltaX
        targetQuadrantCoordinates.y = enterpriseQuadrantCoordinates.y + deltaY

        self._validateCoordinates(coordinate=targetQuadrantCoordinates,
                                  minX=MIN_QUADRANT_X_COORDINATE,
                                  maxX=MAX_QUADRANT_X_COORDINATE,
                                  minY=MIN_QUADRANT_Y_COORDINATE,
                                  maxY=MAX_QUADRANT_Y_COORDINATE)

        self._destinationCoordinates = targetQuadrantCoordinates
        self._warpEffectSection.setup()
        self._warpEffectSection.enabled = True

        schedule(function_pointer=self._checkEffectComplete, interval=1.0)  # type: ignore

    def _doImpulseMove(self, quadrant: Quadrant, enterpriseCoordinates: Coordinates, targetCoordinates: Coordinates):
        """
        Handle impulse move if we are not blocked by any obstacles.

        Args:
            quadrant:               The current quadrant
            enterpriseCoordinates:  Then enterprise sector coordinates
            targetCoordinates:      Where the player indicated we were moving
        """

        self.__updateQuadrant(quadrant=quadrant, currentCoordinates=enterpriseCoordinates, targetCoordinates=targetCoordinates)
        quadrant.enterprise.destinationPoint = GamePiece.gamePositionToScreenPosition(gameCoordinates=targetCoordinates)
        quadrant.enterpriseCoordinates = targetCoordinates
        quadrant.enterprise.inMotion   = True

        self._gameEngine.impulse(newCoordinates=targetCoordinates, quadrant=quadrant, enterprise=quadrant.enterprise)
        self._soundMachine.playSound(SoundType.Impulse)
        if quadrant.klingonCount > 0 or quadrant.commanderCount > 0 or quadrant.superCommanderCount > 0:
            self._gameState.shipCondition = ShipCondition.Red
        else:
            self._gameState.shipCondition = ShipCondition.Green

    def _doBlockedImpulseMove(self, quadrant: Quadrant, enterpriseCoordinates: Coordinates, results: LineOfSightResponse):
        """
        Handle an impulse move where the Enterprise was blocked by an obstacle

        Args:
            quadrant:               The current quadrant
            enterpriseCoordinates:  Then enterprise sector coordinates
            results:                The results from the line of sight query
        """
        self._messageConsole.displayMessage(f'Destination is blocked by: {results.obstacle.id}')
        self._soundMachine.playSound(SoundType.PleaseRepeatRequest)

        baseGamePiece:      BaseGamePiece = cast(BaseGamePiece, results.obstacle)
        blockerCoordinates: Coordinates    = baseGamePiece.gameCoordinates
        stopEnergy:         float          = self._gameEngine.computeEnergyWhenBlocked(startSector=enterpriseCoordinates, endSector=blockerCoordinates)
        self._gameState.energy -= stopEnergy

        directionData: DirectionData = self._determineCloseCoordinatesToBlockedObject(quadrant=quadrant, targetCoordinates=blockerCoordinates)
        self.logger.info(f'Move Enterprise to: {directionData.coordinates}')

        self.__updateQuadrant(quadrant=quadrant, currentCoordinates=enterpriseCoordinates, targetCoordinates=directionData.coordinates)
        quadrant.enterprise.inMotion   = True
        quadrant.enterpriseCoordinates = directionData.coordinates

        self._gameEngine.impulse(newCoordinates=directionData.coordinates, quadrant=quadrant, enterprise=quadrant.enterprise)
        self._soundMachine.playSound(SoundType.EnterpriseBlocked)

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
            obstacles.append(quadrant.planet)
        obstacles.extend(quadrant.klingons)
        obstacles.extend(quadrant.commanders)
        results: LineOfSightResponse = self._hasLineOfSight(startingPoint=startingPoint, endPoint=endPoint, obstacles=obstacles)

        self.logger.info(f'{results=}')
        return results

    def _determineCloseCoordinatesToBlockedObject(self, quadrant: Quadrant, targetCoordinates: Coordinates) -> DirectionData:
        """
        Get Enterprise "Close" coordinates to where it was 'blocked'
        Args:
            quadrant:           The quadrant we are in
            targetCoordinates:

        Returns:
        """
        directionData: DirectionData = self._gameEngine.computeCloseCoordinates(targetCoordinates=targetCoordinates)
        self.logger.info(f'{directionData=}')

        while directionData.coordinates.valid() is False or quadrant.isSectorEmpty(sectorCoordinates=directionData.coordinates) is False:
            directionData = self._gameEngine.computeCloseCoordinates(targetCoordinates=targetCoordinates)
            self.logger.info(f'Try again: {directionData=}')

        return directionData

    # noinspection PyUnusedLocal
    def _checkEffectComplete(self, deltaTime: float):
        """
        This method is scheduled to periodically query to see if the warp effect is done;
        If so the disables the warp effect section and calls the warp travel callback which
        does the actual work of warping the enterprise

        Args:
            deltaTime:
        """
        effectComplete: bool = self._warpEffectSection.isEffectComplete()
        if effectComplete is True:
            print('Warp effect is done')
            unschedule(self._checkEffectComplete)
            self._warpEffectSection.enabled = False
            self._warpTravelCallback(self._destinationCoordinates)

    def _validateCoordinates(self, coordinate: Coordinates, minX: int, maxX: int, minY: int, maxY: int):
        """

        Args:
            coordinate:  The coordinate
            minX:
            maxX:
            minY:
            maxY:

        Returns:  True if coordinate is value;  Else raises exception

        """
        valid: bool = True

        intXCoordinate: int = coordinate.x
        intYCoordinate: int = coordinate.y
        if intXCoordinate < minX or intXCoordinate > maxX:
            raise InvalidCommandValueException(message=f'Invalid X coordinate: {intXCoordinate}. Must be in range {minX},{maxX}')

        if intYCoordinate < minY or intYCoordinate > maxY:
            raise InvalidCommandValueException(message=f'Invalid Y coordinate: {intYCoordinate}. Must be in range {minY},{maxY}')

        return valid

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
        targetSector.sprite = currentSector.sprite
        currentSector.sprite = cast(GamePiece, None)

        return quadrant
