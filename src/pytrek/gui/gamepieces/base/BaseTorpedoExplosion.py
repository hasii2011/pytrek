

from src.pytrek.gui.gamepieces.base.BaseAnimator import BaseAnimator
from src.pytrek.gui.gamepieces.base.BaseAnimator import TextureList


class BaseTorpedoExplosion(BaseAnimator):

    def __init__(self, textureList: TextureList, delayFrames: int, scale: float = 1.0):

        super().__init__(textureList=textureList, delayFrames=delayFrames, scale=scale)
