
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import BaseTorpedoExplosion
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList


class CommanderTorpedoExplosion(BaseTorpedoExplosion):

    DELAY_FRAMES: int = 8

    def __init__(self, textureList: TextureList):

        super().__init__(textureList=textureList, delayFrames=CommanderTorpedoExplosion.DELAY_FRAMES, scale=1.0)
