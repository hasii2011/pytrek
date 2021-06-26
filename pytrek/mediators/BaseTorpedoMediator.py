
from logging import Logger
from logging import getLogger
from typing import cast

from arcade import SpriteList

from pytrek.mediators.BaseMediator import BaseMediator

from pytrek.model.Quadrant import Quadrant


class BaseTorpedoMediator(BaseMediator):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):

        super().__init__()

        self.logger: Logger = BaseTorpedoMediator.clsLogger

        self._torpedoes:        SpriteList = SpriteList()
        self._torpedoFollowers: SpriteList = SpriteList(is_static=True)
        self._misses:           SpriteList = SpriteList()

        self._klingonList:      SpriteList = cast (SpriteList, None)

        self._lastTimeCheck: float = self._gameEngine.gameClock / 1000
        self.logger.info(f'{self._lastTimeCheck=}')

    @property
    def klingonList(self) -> SpriteList:
        return self._klingonList

    @klingonList.setter
    def klingonList(self, newValues: SpriteList):
        self._klingonList = newValues

    @property
    def torpedoes(self) -> SpriteList:
        return self._torpedoes

    @torpedoes.setter
    def torpedoes(self, newList: SpriteList):
        """
        Args:
            newList:
        """
        self._torpedoes = newList

    @property
    def torpedoFollowers(self) -> SpriteList:
        return self._torpedoFollowers

    @torpedoFollowers.setter
    def torpedoFollowers(self, newValues: SpriteList):
        self._torpedoFollowers = newValues

    @property
    def torpedoDuds(self) -> SpriteList:
        return self._misses

    @torpedoDuds.setter
    def torpedoDuds(self, newValues: SpriteList):
        self._misses = newValues

    def draw(self):
        """
        Implemented by subclass
        """
        pass

    def update(self, quadrant: Quadrant):
        """
        Implemented by subclass
        Args:
            quadrant:
        """
        pass
