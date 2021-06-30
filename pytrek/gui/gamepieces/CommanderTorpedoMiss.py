
from pytrek.gui.gamepieces.BasicMiss import BasicMiss


class CommanderTorpedoMiss(BasicMiss):

    FILENAME:        str = "CommanderTorpedoMiss.png"

    def __init__(self, placedTime: float):

        super().__init__(fileName=CommanderTorpedoMiss.FILENAME, placedTime=placedTime, scale=0.1)
