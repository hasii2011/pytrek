
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import BaseTorpedoExplosion
from pytrek.gui.gamepieces.base.BaseTorpedoExplosion import TextureList


class PhotonTorpedoExplosion(BaseTorpedoExplosion):

    DELAY_FRAMES: int = 8

    def __init__(self, textureList: TextureList):

        super().__init__(textureList=textureList, delayFrames=PhotonTorpedoExplosion.DELAY_FRAMES, scale=0.5)

