
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import BaseTorpedoExplosion
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList


class SuperCommanderTorpedoExplosion(BaseTorpedoExplosion):

    DELAY_FRAMES: int = 16

    def __init__(self, textureList: TextureList):

        super().__init__(textureList=textureList, delayFrames=SuperCommanderTorpedoExplosion.DELAY_FRAMES, scale=1.0)
