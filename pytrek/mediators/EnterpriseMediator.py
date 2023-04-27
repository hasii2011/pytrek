
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import SpriteList
from arcade import View
from arcade import Window
from arcade import color

from arcade import schedule
from arcade import unschedule

from pytrek.SoundMachine import SoundMachine
from pytrek.SoundMachine import SoundType
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.DirectionData import DirectionData
from pytrek.engine.ShipCondition import ShipCondition

from pytrek.gui.UITypes import WarpTravelCallback
from pytrek.gui.WarpEffect import WarpEffect
from pytrek.gui.WarpDialog import DialogAnswer
from pytrek.gui.WarpDialog import WarpTravelAnswer
from pytrek.gui.WarpDialog import WarpDialog

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

    def __init__(self, view: View, warpTravelCallback: WarpTravelCallback):
        """

        Args:
            view:   The view to restore
            warpTravelCallback:
        """

        super().__init__()

        self._view:               View = view
        self._warpTravelCallback: WarpTravelCallback = warpTravelCallback

        self.logger:                  Logger       = getLogger(__name__)
        self._soundMachine:           SoundMachine = SoundMachine()
        self._warpSpeed:              float        = 0.0
        self._warpEffect:             WarpEffect   = cast(WarpEffect, None)
        self._destinationCoordinates: Coordinates = cast(Coordinates, None)

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

    def warp(self):
        #
        # Get warp speed and target quadrant coordinates from user
        # Stub out for now
        warpTravelDialog: WarpDialog = WarpDialog(window=self._view.window, completeCallback=self._warpTravelDialogComplete)    # type: ignore

        self._view.window.show_view(warpTravelDialog)   # type: ignore

    def _warpTravelDialogComplete(self, warpTravelAnswer: WarpTravelAnswer):
        """
        The callback when we get an answer on whether we are traveling to
        another quadrant

        Args:
            warpTravelAnswer:  The answer with data if answered `Ok`
        """
        if warpTravelAnswer.dialogAnswer == DialogAnswer.Ok:
            self._warpSpeed              = warpTravelAnswer.warpFactor
            self._destinationCoordinates = warpTravelAnswer.coordinates

            viewWindow:   Window = self._view.window        # type: ignore
            screenWidth:  int    = viewWindow.width
            screenHeight: int    = viewWindow.height
            warpEffect: WarpEffect = WarpEffect(screenWidth=screenWidth, screenHeight=screenHeight)

            viewWindow.show_view(warpEffect)

            warpEffect.setup()
            self._warpEffect = warpEffect
            # I do not know what a Number is  tell mypy so
            schedule(function_pointer=self.doWarpWhenEffectComplete, interval=1.0)  # type: ignore
        else:
            self._view.window.show_view(self._view)     # type: ignore

        self._view.window.background_color = color.BLACK    # type: ignore

    def doWarpWhenEffectComplete(self, deltaTime: float):

        effectComplete: bool = self._warpEffect.isEffectComplete()

        self.logger.info(f'Is warp effect complete {deltaTime} {effectComplete=}')

        if effectComplete is True:
            unschedule(self.doWarpWhenEffectComplete)
            self._view.window.show_view(self._view)     # type: ignore
            #
            # Callback to someone (presumably top level view) to let them know
            # it is time to warp;
            #
            self._warpTravelCallback(self._warpSpeed, self._destinationCoordinates)

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
