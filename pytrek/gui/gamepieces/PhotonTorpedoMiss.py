
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss


class EnterpriseTorpedoMiss(BaseMiss):

    FILENAME:        str = "PhotonTorpedoMiss.png"

    def __init__(self, placedTime: float):

        super().__init__(fileName=EnterpriseTorpedoMiss.FILENAME, placedTime=placedTime)
