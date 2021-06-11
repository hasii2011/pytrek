
from logging import Logger
from logging import getLogger


from pytrek.gui.gamepieces.BaseGamePiece import BaseGamePiece


class BasicMiss(BaseGamePiece):

    def __init__(self, fileName: str, placedTime: float):

        super().__init__(fileName)

        self.logger:     Logger = getLogger(__name__)
        self._placedTime: float = placedTime

    @property
    def placedTime(self) -> float:
        """

        Returns:  When the sprite was placed on the board

        """
        return self._placedTime
