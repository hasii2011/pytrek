
from logging import Logger
from logging import getLogger

from pytrek.gui.gamepieces.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.GamePieceTypes import EnemyTorpedoId
from pytrek.gui.gamepieces.KlingonTorpedoFollower import KlingonTorpedoFollower


class KlingonTorpedo(BaseEnemyTorpedo):

    FILENAME: str = 'KlingonTorpedo.png'

    nextId: int = 0

    def __init__(self):

        torpedoId: EnemyTorpedoId = EnemyTorpedoId(f'KlingonTorpedo-{KlingonTorpedo.nextId}')
        KlingonTorpedo.nextId += 1

        super().__init__(filename=KlingonTorpedo.FILENAME, torpedoId=torpedoId)
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
