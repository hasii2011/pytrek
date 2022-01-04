from enum import Enum
from logging import Logger
from logging import getLogger

from arcade import Sound

from pytrek.LocateResources import LocateResources
from pytrek.Singleton import Singleton
from pytrek.settings.GameSettings import GameSettings


class SoundType(Enum):
    UnableToComply = 'UnableToComply.wav'
    Docked         = 'Docked.wav'
    PhaserFire     = 'PhaserFire.wav'


class SoundMachine(Singleton):

    # noinspection SpellCheckingInspection
    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        self._gameSettings: GameSettings = GameSettings()

        self._unableToComply: Sound = self.loadSound(bareFileName=SoundType.UnableToComply.value)
        self._docked:         Sound = self.loadSound(bareFileName=SoundType.Docked.value)
        self._phaser:         Sound = self.loadSound(bareFileName=SoundType.PhaserFire.value)

    def loadSound(self, bareFileName: str) -> Sound:
        """

        Args:
            bareFileName:
        """
        fqFileName: str   = LocateResources.getResourcesPath(LocateResources.SOUND_RESOURCES_PACKAGE_NAME, bareFileName)
        sound:      Sound = Sound(fqFileName)

        return sound

    def playSound(self, soundType: SoundType):
        """

        Args:
            soundType:
        """
        if soundType == SoundType.UnableToComply:
            self._unableToComply.play(volume=self._gameSettings.soundVolume.value)
        elif soundType == SoundType.Docked:
            self._docked.play(volume=self._gameSettings.soundVolume.value)
        elif soundType == SoundType.PhaserFire:
            self._phaser.play(volume=self._gameSettings.soundVolume.value)
