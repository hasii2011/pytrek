
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import SpriteList

from pytrek.Constants import SOUND_VOLUME_HIGH
from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.engine.Computer import Computer
from pytrek.gui.MessageConsole import MessageConsole
from pytrek.gui.gamepieces.Enterprise import Enterprise

from pytrek.gui.gamepieces.GamePieceTypes import Klingons
from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.gui.gamepieces.PhotonTorpedo import PhotonTorpedo
from pytrek.model.Quadrant import Quadrant


class PhotonTorpedoMediator:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._computer:       Computer       = Computer()
        self._messageConsole: MessageConsole = MessageConsole()

        self._torpedoes:      SpriteList     = cast(SpriteList, None)

        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName='tos_photon_torpedo.wav')

        self._photonTorpedoFired: Sound = Sound(file_name=fqFileName)

    @property
    def torpedoes(self) -> SpriteList:
        return self._torpedoes

    @torpedoes.setter
    def torpedoes(self, newValues: SpriteList):
        self._torpedoes = newValues

    # noinspection PyUnusedLocal
    def draw(self, quadrant: Quadrant):
        self.torpedoes.draw()

    # noinspection PyUnusedLocal
    def update(self, quadrant: Quadrant):
        self.torpedoes.update()

    def fireEnterpriseTorpedoesAtKlingons(self, enterprise: Enterprise, klingons: Klingons):

        self._messageConsole.displayMessage("Firing Torpedoes!!")

        if len(klingons) == 0:
            self._messageConsole.displayMessage("Don't waste torpedoes.  Nothing to fire at")
        else:
            self._pointAtKlingon(enterprise=enterprise, klingon=klingons[0])
            self._fireTorpedo(enterprise=enterprise, klingon=klingons[0])
            self._photonTorpedoFired.play(volume=SOUND_VOLUME_HIGH)

    def _pointAtKlingon(self, klingon: Klingon, enterprise: Enterprise):

        currentPoint:     ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        destinationPoint: ArcadePoint = ArcadePoint(x=klingon.center_x, y=klingon.center_y)

        normalAngle: float = self._computer.computeAngleToTarget(shooter=currentPoint, deadMeat=destinationPoint)
        enterprise.angle = normalAngle + 125

        self.logger.info(f'{enterprise.angle=}')

    def _fireTorpedo(self, enterprise: Enterprise, klingon: Klingon):

        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)
        klingonPoint:    ArcadePoint = ArcadePoint(x=klingon.center_x,    y=klingon.center_y)

        torpedo: PhotonTorpedo = PhotonTorpedo()

        torpedo.center_x = enterprisePoint.x
        torpedo.center_y = enterprisePoint.y
        torpedo.inMotion = True
        torpedo.destinationPoint = klingonPoint

        self.torpedoes.append(torpedo)
        self._messageConsole.displayMessage(f'Enterprise fire from: {enterprise.currentPosition} at Klingon {klingon.currentPosition}')
