
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import EnemyFollowerId
from pytrek.gui.gamepieces.GamePieceTypes import EnemyTorpedoId


class KlingonTorpedoFollower(GamePiece):

    FILENAME: str = 'KlingonTorpedoFollower.png'

    nextId: int = 0

    def __init__(self):

        super().__init__(filename=KlingonTorpedoFollower.FILENAME, scale=0.1)

        KlingonTorpedoFollower.nextId += 1

        self._id:       EnemyFollowerId = EnemyFollowerId(f'KlingonTorpedoFollower-{KlingonTorpedoFollower.nextId}')
        self._following: EnemyTorpedoId = EnemyTorpedoId('')

    @property
    def id(self) -> EnemyFollowerId:
        return self._id

    @property
    def following(self) -> EnemyTorpedoId:
        """
        """
        return self._following

    @following.setter
    def following(self, newValue: EnemyTorpedoId):
        """
        Args:
            newValue:
        """
        self._following = newValue
