
from pytrek.gui.gamepieces.BasicMiss import BasicMiss


class KlingonTorpedoMiss(BasicMiss):

    DISPLAY_SECONDS: int = 5
    FILENAME:        str = "KlingonTorpedoMiss.png"

    def __init__(self, playTime: float):

        super().__init__(fileName=KlingonTorpedoMiss.FILENAME, playTime=playTime)
