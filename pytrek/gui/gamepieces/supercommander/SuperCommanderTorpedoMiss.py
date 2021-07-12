
from pytrek.gui.gamepieces.base.BaseMiss import BaseMiss


class SuperCommanderTorpedoMiss(BaseMiss):

    FILENAME:        str = "SuperCommanderTorpedoMiss.png"

    def __init__(self, placedTime: float):

        super().__init__(fileName=SuperCommanderTorpedoMiss.FILENAME, placedTime=placedTime, scale=0.1)
