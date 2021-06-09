
from logging import Logger
from logging import getLogger


from pytrek.gui.gamepieces.BaseGamePiece import BaseGamePiece


class BasicMiss(BaseGamePiece):

    def __init__(self, fileName: str, playTime: float):

        super().__init__(fileName)

        self.logger:           Logger = getLogger(__name__)
        self.displayTime:      float  = playTime
        self.eligibleToRemove: bool   = False
