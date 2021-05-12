
from typing import cast

from logging import Logger
from logging import getLogger

from uuid import uuid4

from arcade import SpriteList

from pytrek.LocateResources import LocateResources

from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.engine.Computer import Computer

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.KlingonTorpedoFollower import KlingonTorpedoFollower
from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion

from pytrek.model.Coordinates import Coordinates


class KlingonTorpedo(GamePiece, SmoothMotion):

    def __init__(self):

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='KlingonTorpedo.png')

        GamePiece.__init__(self, filename=fqFileName)
        SmoothMotion.__init__(self)

        self.logger: Logger = getLogger(__name__)

        self._computer: Computer = Computer()

        self._uuid:              uuid4        = uuid4()
        self._firedFromPosition: Coordinates = cast(Coordinates, None)
        self._followers:         SpriteList  = cast(SpriteList, None)

    @property
    def uuid(self) -> uuid4:
        return self._uuid

    @property
    def firedFromPosition(self) -> Coordinates:
        return self._firedFromPosition

    @firedFromPosition.setter
    def firedFromPosition(self, newValue: Coordinates):
        self._firedFromPosition = newValue
        self.currentPosition    = newValue

    def followers(self, newValues: SpriteList):
        """
        Reference back to global follower list

        Args:
            newValues:
        """
        self._followers = newValues

    followers = property(None, followers)

    def update(self):

        if self.inMotion is True:
            actualAngleRadians, angleDiffRadians = self.computeArcadeMotion(currentPoint=ArcadePosition(x=self.center_x, y=self.center_y),
                                                                            destinationPoint=self.destinationPoint,
                                                                            spriteRotationAngle=self.angle,
                                                                            rotationalSpeed=self.rotationSpeed)
            self.doMotion(gamePiece=self, destinationPoint=self.destinationPoint, angleDiffRadians=angleDiffRadians, actualAngleRadians=actualAngleRadians)
        else:
            self._removeMyFollowers()

        self._potentiallyCreateAFollower()

    def _removeMyFollowers(self):

        for follower in self._followers:
            follower: KlingonTorpedoFollower = cast(KlingonTorpedoFollower, follower)
            if follower.following == self._uuid:
                self._followers.remove(follower)

    def _potentiallyCreateAFollower(self):
        """
        Only create one if we have entered another sector
        """
        currentX: float = self.center_x
        currentY: float = self.center_y
        position: Coordinates = self._computer.computeSectorCoordinates(x=currentX, y=currentY)

        if position != self.currentPosition:
            self.logger.debug(f'Created a follower @ {position}')
            self._placeTorpedoFollower(x=currentX, y=currentY)
            self.currentPosition = position

    def _placeTorpedoFollower(self, x: float, y: float):

        klingonTorpedoFollower: KlingonTorpedoFollower = KlingonTorpedoFollower()

        klingonTorpedoFollower.center_x  = x
        klingonTorpedoFollower.center_y  = y
        klingonTorpedoFollower.following = self._uuid

        self._followers.append(klingonTorpedoFollower)
