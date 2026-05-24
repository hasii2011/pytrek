
from pytrek.gui.gamepieces.base.BaseTorpedoFollower import BaseTorpedoFollower

from pytrek.gui.gamepieces.GamePieceTypes import EnemyFollowerId


class SuperCommanderTorpedoFollower(BaseTorpedoFollower):

    FILENAME: str = 'SuperCommanderTorpedoFollower.png'

    nextId: int = 0

    def __init__(self):

        followerId: EnemyFollowerId = EnemyFollowerId(f'SuperCommanderTorpedoFollower-{SuperCommanderTorpedoFollower.nextId}')

        super().__init__(filename=SuperCommanderTorpedoFollower.FILENAME, followerId=followerId, scale=0.7)

        SuperCommanderTorpedoFollower.nextId += 1
