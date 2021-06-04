
from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.Constants import SOUND_VOLUME_HIGH
from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.mediators.BaseMediator import BaseMediator
from pytrek.model.Coordinates import Coordinates
from pytrek.model.Quadrant import Quadrant


class EnterpriseMediator(BaseMediator):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._loadSounds()

    def update(self, quadrant: Quadrant):

        enterprise: Enterprise = quadrant.enterprise

        arcadeX, arcadeY = GamePiece.gamePositionToScreenPosition(quadrant.enterpriseCoordinates)
        if enterprise.inMotion is True:

            self.logger.debug(f'Enterprise arcade position: ({arcadeX},{arcadeY})')
            enterprise.destinationPoint = ArcadePoint(x=arcadeX, y=arcadeY)
            enterprise.update()
        else:
            enterprise.center_x = arcadeX
            enterprise.center_y = arcadeY

    def impulse(self, quadrant: Quadrant, arcadePoint: ArcadePoint):

        coordinates: Coordinates = self._computer.computeSectorCoordinates(x=arcadePoint.x, y=arcadePoint.y)

        if coordinates == self._gameState.currentSectorCoordinates:
            self._messageConsole.displayMessage("WTF.  You are already here!")
            self._soundUnableToComply.play(volume=SOUND_VOLUME_HIGH)
        else:
            quadrant.enterprise.inMotion    = True
            quadrant.enterpriseCoordinates = coordinates
            self._gameEngine.impulse(newCoordinates=coordinates, quadrant=quadrant, enterprise=quadrant.enterprise)
            self._soundImpulse.play(volume=SOUND_VOLUME_HIGH)

        # StarTrekScreen.quitIfTimeExpired()
        # self._dockIfAdjacentToStarbase()

    def warp(self):
        pass

    def _loadSounds(self):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName='impulse.wav')
        self._soundImpulse: Sound = Sound(file_name=fqFileName)

        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName='unableToComply.wav')
        self._soundUnableToComply: Sound = Sound(file_name=fqFileName)
