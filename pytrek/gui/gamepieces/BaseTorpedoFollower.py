
from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import EnemyFollowerId
from pytrek.gui.gamepieces.GamePieceTypes import EnemyTorpedoId


class BaseTorpedoFollower(GamePiece):

    def __init__(self, filename: str, followerId: EnemyFollowerId, scale: float = 1.0):

        super().__init__(filename=filename, scale=scale)

        self._id:        EnemyFollowerId = followerId
        self._following: EnemyTorpedoId  = EnemyTorpedoId('')

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
