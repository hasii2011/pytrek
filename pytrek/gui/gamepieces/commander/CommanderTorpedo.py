from logging import Logger, getLogger

from pytrek.gui.gamepieces.base.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.commander.CommanderTorpedoFollower import CommanderTorpedoFollower
from pytrek.gui.gamepieces.GamePieceTypes import EnemyTorpedoId


class CommanderTorpedo(BaseEnemyTorpedo):

    FILENAME: str = 'CommanderTorpedo.png'

    nextId: int = 0

    def __init__(self, speed: float = 3.0):

        torpedoId: EnemyTorpedoId = EnemyTorpedoId(f'CommanderTorpedo-{CommanderTorpedo.nextId}')

        CommanderTorpedo.nextId += 1

        super().__init__(filename=CommanderTorpedo.FILENAME, speed=speed, torpedoId=torpedoId, scale=0.4)

        self.logger: Logger = getLogger(__name__)

    def _placeTorpedoFollower(self, x: float, y: float):
        """
        We implement the empty base class method

        Args:
            x:  Arcade x
            y:  Arcade y
        """
        commanderTorpedoFollower: CommanderTorpedoFollower = CommanderTorpedoFollower()

        commanderTorpedoFollower.center_x  = x
        commanderTorpedoFollower.center_y  = y
        commanderTorpedoFollower.following = self._id

        self._followers.append(commanderTorpedoFollower)
