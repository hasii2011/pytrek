

from uuid import uuid4

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.GamePieceTypes import EnemyTorpedoId


class KlingonTorpedoFollower(GamePiece):

    FILENAME: str = 'KlingonTorpedoFollower.png'

    def __init__(self):

        super().__init__(filename=KlingonTorpedoFollower.FILENAME, scale=0.1)

        self._uuid:      uuid4 = uuid4()            # My ID
        self._following: EnemyTorpedoId   = EnemyTorpedoId('')

    @property
    def uuid(self) -> uuid4:
        return self._uuid

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

