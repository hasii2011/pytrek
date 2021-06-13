
from pytrek.gui.gamepieces.BasicMiss import BasicMiss


class PhotonTorpedoMiss(BasicMiss):

    FILENAME:        str = "PhotonTorpedoMiss.png"

    def __init__(self, placedTime: float):

        super().__init__(fileName=PhotonTorpedoMiss.FILENAME, placedTime=placedTime)
