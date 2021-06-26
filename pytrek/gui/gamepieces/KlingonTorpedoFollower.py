
from pytrek.gui.gamepieces.BaseTorpedoFollower import BaseTorpedoFollower
from pytrek.gui.gamepieces.GamePieceTypes import EnemyFollowerId


class KlingonTorpedoFollower(BaseTorpedoFollower):

    FILENAME: str = 'KlingonTorpedoFollower.png'

    nextId: int = 0

    def __init__(self):

        followerId: EnemyFollowerId = EnemyFollowerId(f'KlingonTorpedoFollower-{KlingonTorpedoFollower.nextId}')

        super().__init__(filename=KlingonTorpedoFollower.FILENAME, followerId=followerId, scale=0.1)

        KlingonTorpedoFollower.nextId += 1
