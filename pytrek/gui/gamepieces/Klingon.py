
from typing import NewType
from typing import cast

from pytrek.LocateResources import LocateResources
from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.model.Coordinates import Coordinates

from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion


KlingonId       = NewType('KlingonId', str)


class Klingon(GamePiece, SmoothMotion):

    def __init__(self, coordinates: Coordinates):
        """

        Args:
            coordinates:   Current Game Position
        """
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName='KlingonD7.png')

        GamePiece.__init__(self, filename=fqFileName)
        SmoothMotion.__init__(self)

        self.currentPosition = coordinates

        self._power:          float     = cast(float, None)
        self._firingInterval: int       = cast(int, None)
        self._lastTimeCheck:  int       = cast(int, None)
        self._id:             KlingonId = KlingonId(f'Klingon-{self.currentPosition}')

    @property
    def power(self) -> float:
        return self._power

    @power.setter
    def power(self, theNewValue: float):
        self._power = theNewValue

    @property
    def firingInterval(self) -> int:
        return self._firingInterval

    @firingInterval.setter
    def firingInterval(self, newValue: int):
        self._firingInterval = newValue

    @property
    def lastTimeCheck(self) -> int:
        return self._lastTimeCheck

    @lastTimeCheck.setter
    def lastTimeCheck(self, newValue: int):
        self._lastTimeCheck = newValue

    @property
    def id(self) -> KlingonId:
        return self._id

    @id.setter
    def id(self, newValue: KlingonId):
        self._id = newValue

    def __str__(self):

        lookAtMe: str = (
            f'Klingon['
            f'{self.id=} '
            f'power={self.power:.3f} '
            f'firingInterval={self.firingInterval} '
            f'{self.currentPosition=}'
            ']'
        )
        return lookAtMe

    def __repr__(self):
        return self.__str__()
