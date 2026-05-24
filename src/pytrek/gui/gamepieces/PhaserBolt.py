
from pytrek.gui.gamepieces.base.BaseAnimator import BaseAnimator
from pytrek.gui.gamepieces.base.BaseAnimator import TextureList


class PhaserBolt(BaseAnimator):

    DELAY_FRAMES: int = 8

    def __init__(self, textureList: TextureList):

        super().__init__(textureList=textureList, delayFrames=PhaserBolt.DELAY_FRAMES, scale=0.5)
