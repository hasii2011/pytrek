
from logging import Logger
from logging import getLogger

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.GamePieceTypes import EnemyTorpedoId
from pytrek.gui.gamepieces.klingon.KlingonTorpedoFollower import KlingonTorpedoFollower


class KlingonTorpedo(BaseEnemyTorpedo):

    FILENAME: str = 'KlingonTorpedo.png'

    nextId: int = 0

    def __init__(self, speed: float = 3.0):

        torpedoId: EnemyTorpedoId = EnemyTorpedoId(f'KlingonTorpedo-{KlingonTorpedo.nextId}')
        KlingonTorpedo.nextId += 1

        super().__init__(filename=KlingonTorpedo.FILENAME, torpedoId=torpedoId, speed=speed)
        self.logger: Logger = getLogger(__name__)

    def _placeTorpedoFollower(self, x: float, y: float):
        """
        We implement the empty base class method

        Args:
            x:  Arcade x
            y:  Arcade y
        """

        klingonTorpedoFollower: KlingonTorpedoFollower = KlingonTorpedoFollower()

        klingonTorpedoFollower.center_x  = x
        klingonTorpedoFollower.center_y  = y
        klingonTorpedoFollower.following = self._id

        self._followers.append(klingonTorpedoFollower)
