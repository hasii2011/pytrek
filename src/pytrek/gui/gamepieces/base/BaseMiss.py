
from logging import Logger
from logging import getLogger


from pytrek.gui.gamepieces.base.BaseGamePiece import BaseGamePiece


class BaseMiss(BaseGamePiece):

    def __init__(self, fileName: str, placedTime: float, scale: float = 1.0):

        super().__init__(filename=fileName, scale=scale)

        self.logger:     Logger = getLogger(__name__)
        self._placedTime: float = placedTime

    @property
    def placedTime(self) -> float:
        """

        Returns:  When the sprite was placed on the board

        """
        return self._placedTime
