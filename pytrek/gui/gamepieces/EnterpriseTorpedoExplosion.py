
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import BaseTorpedoExplosion
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList


class EnterpriseTorpedoExplosion(BaseTorpedoExplosion):

    DELAY_FRAMES: int = 8

    def __init__(self, textureList: TextureList):

        super().__init__(textureList=textureList, delayFrames=EnterpriseTorpedoExplosion.DELAY_FRAMES, scale=0.5)

