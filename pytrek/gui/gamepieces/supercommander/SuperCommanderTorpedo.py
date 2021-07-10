
from logging import Logger
from logging import getLogger

from pytrek.gui.gamepieces.GamePieceTypes import EnemyTorpedoId

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo


class SuperCommanderTorpedo(BaseEnemyTorpedo):
    FILENAME: str = 'SuperCommanderTorpedo.png'

    nextId: int = 0

    def __init__(self, speed: float = 3.0):

        torpedoId: EnemyTorpedoId = EnemyTorpedoId(f'SuperCommanderTorpedo-{SuperCommanderTorpedo.nextId}')

        SuperCommanderTorpedo.nextId += 1

        super().__init__(filename=SuperCommanderTorpedo.FILENAME, speed=speed, torpedoId=torpedoId, scale=0.15)

        self.logger: Logger = getLogger(__name__)
