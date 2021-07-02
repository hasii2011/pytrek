
from pytrek.gui.gamepieces.BaseMiss import BaseMiss


class PhotonTorpedoMiss(BaseMiss):

    FILENAME:        str = "PhotonTorpedoMiss.png"

    def __init__(self, placedTime: float):

        super().__init__(fileName=PhotonTorpedoMiss.FILENAME, placedTime=placedTime)
