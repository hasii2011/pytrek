
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.engine.ArcadePoint import ArcadePoint
from pytrek.gui.gamepieces.BaseEnemyTorpedo import BaseEnemyTorpedo
from pytrek.gui.gamepieces.CommanderTorpedo import CommanderTorpedo
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import Enemy
from pytrek.mediators.BaseTorpedoMediator import BaseTorpedoMediator

from pytrek.model.Quadrant import Quadrant


class CommanderTorpedoMediator(BaseTorpedoMediator):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__()

        self._soundCommanderTorpedo: Sound = cast(Sound, None)

        self._loadSounds()

    def draw(self):
        """
        We must implement this
        """
        self.torpedoes.draw()
        self.torpedoFollowers.draw()
        self.torpedoDuds.draw()

    def update(self, quadrant: Quadrant):
        """
        We must implement this

        Args:
            quadrant:
        """
        self._fireTorpedoesAtEnterpriseIfNecessary(quadrant=quadrant, enemies=quadrant.commanders)
        self.torpedoes.update()

        self._handleTorpedoMisses(quadrant)

    def _getTorpedoToFire(self, enemy: Enemy, enterprise: Enterprise) -> BaseEnemyTorpedo:
        """
        Must be implemented by subclass to create correct type of torpedo

        Args:
            enemy:      The Klingon, Commander, or Super Commander that is firing
            enterprise: Where Captain Kirk is waiting

        Returns:  A torpedo of the correct kind
        """
        klingonPoint:    ArcadePoint = ArcadePoint(x=enemy.center_x, y=enemy.center_y)
        enterprisePoint: ArcadePoint = ArcadePoint(x=enterprise.center_x, y=enterprise.center_y)

        commanderTorpedo: CommanderTorpedo = CommanderTorpedo()

        commanderTorpedo.center_x = klingonPoint.x
        commanderTorpedo.center_y = klingonPoint.y
        commanderTorpedo.inMotion = True
        commanderTorpedo.destinationPoint  = enterprisePoint
        commanderTorpedo.firedFromPosition = enemy.gameCoordinates
        commanderTorpedo.firedBy   = enemy.id
        commanderTorpedo.followers = self.torpedoFollowers

        return commanderTorpedo

    def _playCannotFireSound(self):
        """
        We must implement this
        """
        pass

    def _playTorpedoFiredSound(self):
        """
        We must implement this
        """
        self._soundCommanderTorpedo.play(self._gameSettings.soundVolume.value)

    def _loadSounds(self):

        self._soundCommanderTorpedo = self._loadSound(bareFileName='CommanderTorpedo.wav')
