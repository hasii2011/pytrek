
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import BaseTorpedoExplosion
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList


class KlingonTorpedoExplosion(BaseTorpedoExplosion):

    DELAY_FRAMES: int = 40

    def __init__(self, textureList: TextureList):

        super().__init__(textureList=textureList, delayFrames=KlingonTorpedoExplosion.DELAY_FRAMES, scale=1.0)
