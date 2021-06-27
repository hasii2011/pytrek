
from logging import Logger
from logging import getLogger

from pytrek.mediators.BaseTorpedoMediator import BaseTorpedoMediator

from pytrek.model.Quadrant import Quadrant


class CommanderTorpedoMediator(BaseTorpedoMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__()

    def draw(self):
        """
        We must implement this
        """
        pass

    def update(self, quadrant: Quadrant):
        """
        We must implement this

        Args:
            quadrant:
        """
        pass
