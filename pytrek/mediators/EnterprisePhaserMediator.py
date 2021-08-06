
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.LocateResources import LocateResources
from pytrek.gui.MessageConsole import MessageConsole

from pytrek.gui.gamepieces.GamePieceTypes import Enemies

from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings


class EnterprisePhaserMediator:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._gameSettings:   GameSettings  = GameSettings()
        self._messageConsole: MessageConsole = MessageConsole()

        self._soundPhaser:         Sound = cast(Sound, None)
        self._soundUnableToComply: Sound = cast(Sound, None)

        self._loadSounds()

    def firePhasers(self, quadrant: Quadrant):

        enemies: Enemies = Enemies([])
        enemies.extend(quadrant.klingons)
        enemies.extend(quadrant.commanders)
        enemies.extend(quadrant.superCommanders)

        if len(enemies) == 0:
            self._soundUnableToComply.play(volume=self._gameSettings.soundVolume.value)
            self._messageConsole.displayMessage("Nothing to fire at")
        else:
            self._soundPhaser.play(volume=self._gameSettings.soundVolume.value)

    def _loadSounds(self):
        self._soundPhaser         = self._loadSound('PhaserFire.wav')
        self._soundUnableToComply = self._loadSound(bareFileName='unableToComply.wav')

    def _loadSound(self, bareFileName: str) -> Sound:

        fqFileName: str = LocateResources.getResourcesPath(LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName)
        sound: Sound = Sound(fqFileName)

        return sound
