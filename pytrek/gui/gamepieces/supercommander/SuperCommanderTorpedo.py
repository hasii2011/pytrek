
from logging import Logger
from logging import getLogger

from pytrek.gui.gamepieces.GamePieceTypes import EnemyTorpedoId

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.supercommander.SuperCommanderTorpedoFollower import SuperCommanderTorpedoFollower


class SuperCommanderTorpedo(BaseEnemyTorpedo):
    FILENAME: str = 'SuperCommanderTorpedo.png'

    nextId: int = 0

    def __init__(self, speed: float = 3.0):

        torpedoId: EnemyTorpedoId = EnemyTorpedoId(f'SuperCommanderTorpedo-{SuperCommanderTorpedo.nextId}')

        SuperCommanderTorpedo.nextId += 1

        super().__init__(filename=SuperCommanderTorpedo.FILENAME, speed=speed, torpedoId=torpedoId, scale=0.15)

        self.logger: Logger = getLogger(__name__)

    def _placeTorpedoFollower(self, x: float, y: float):
        """
        We implement the empty base class method

        Args:
            x:  Arcade x
            y:  Arcade y
        """
        superCommanderTorpedoFollower: SuperCommanderTorpedoFollower = SuperCommanderTorpedoFollower()

        superCommanderTorpedoFollower.center_x  = x
        superCommanderTorpedoFollower.center_y  = y
        superCommanderTorpedoFollower.following = self._id

        self._followers.append(superCommanderTorpedoFollower)
