
from pytrek.gui.gamepieces.BasicMiss import BasicMiss


class KlingonTorpedoMiss(BasicMiss):

    FILENAME:        str = "KlingonTorpedoMiss.png"

    def __init__(self, placedTime: float):

        super().__init__(fileName=KlingonTorpedoMiss.FILENAME, placedTime=placedTime)
