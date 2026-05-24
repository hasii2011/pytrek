
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss


class KlingonTorpedoMiss(BaseMiss):

    FILENAME:        str = "KlingonTorpedoMiss.png"

    def __init__(self, placedTime: float):

        super().__init__(fileName=KlingonTorpedoMiss.FILENAME, placedTime=placedTime)
