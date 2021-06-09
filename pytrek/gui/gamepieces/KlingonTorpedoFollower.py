
from typing import cast

from uuid import uuid4

from pytrek.gui.gamepieces.GamePiece import GamePiece


class KlingonTorpedoFollower(GamePiece):

    FILENAME: str = 'KlingonTorpedoFollower-16.png'

    def __init__(self):

        super().__init__(filename=KlingonTorpedoFollower.FILENAME)

        self._uuid:      uuid4 = uuid4()            # My ID
        self._following: uuid4 = cast(uuid4, None)

    @property
    def uuid(self) -> uuid4:
        return self._uuid

    @property
    def following(self) -> uuid4:
        """
        """
        return self._following

    @following.setter
    def following(self, newValue: uuid4):
        """
        Args:
            newValue:
        """
        self._following = newValue

