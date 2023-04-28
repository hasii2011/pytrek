
from typing import Dict
from typing import NewType

from logging import Logger
from logging import getLogger

from enum import Enum

from hasiihelper.Singleton import Singleton
from arcade import Sound

from pytrek.LocateResources import LocateResources

from pytrek.settings.GameSettings import GameSettings


class SoundType(Enum):
    UnableToComply      = 'UnableToComply.wav'
    Docked              = 'Docked.wav'
    PhaserFired         = 'PhaserFired.wav'
    PleaseRepeatRequest = 'PleaseRepeatRequest.wav'
    Impulse             = 'Impulse.wav'
    EnterpriseBlocked   = 'EnterpriseBlocked.wav'
    PhotonTorpedoFired  = 'PhotonTorpedoFired.wav'
    PhotonTorpedoExploded = 'PhotonTorpedoExploded.wav'
    PhotonTorpedoMisfire  = 'PhotonTorpedoMisfire.wav'
    PhotonTorpedoMiss     = 'PhotonTorpedoMiss.wav'
    Inaccurate            = 'Inaccurate.wav'
    KlingonMove           = 'KlingonMove.wav'
    KlingonTorpedo        = 'KlingonTorpedo.wav'
    KlingonCannotFire     = 'KlingonCannotFire.wav'
    CommanderMove         = 'CommanderMove.wav'
    CommanderTorpedo      = 'CommanderTorpedo.wav'
    CommanderCannotFire   = 'CommanderCannotFire.wav'
    SuperCommanderMove       = 'SuperCommanderMove.wav'
    SuperCommanderTorpedo    = 'SuperCommanderTorpedo.wav'
    SuperCommanderCannotFire = 'SuperCommanderCannotFire.wav'
    Warp                  = 'Warp.wav'
    ShieldHit             = 'ShieldHit.wav'


SoundDictionary = NewType('SoundDictionary', Dict[SoundType, Sound])


class SoundMachine(Singleton):

    # noinspection PyAttributeOutsideInit
    def init(self, *args, **kwargs):

        self.logger: Logger = getLogger(__name__)

        self._gameSettings: GameSettings = GameSettings()

        self._unableToComply:        Sound = self.loadSound(bareFileName=SoundType.UnableToComply.value)
        self._docked:                Sound = self.loadSound(bareFileName=SoundType.Docked.value)
        self._phaserFired:           Sound = self.loadSound(bareFileName=SoundType.PhaserFired.value)
        self._pleaseRepeatRequest:   Sound = self.loadSound(bareFileName=SoundType.PleaseRepeatRequest.value)
        self._impulse:               Sound = self.loadSound(bareFileName=SoundType.Impulse.value)
        self._enterpriseBlocked:     Sound = self.loadSound(bareFileName=SoundType.EnterpriseBlocked.value)
        self._photonTorpedoFired:    Sound = self.loadSound(bareFileName=SoundType.PhotonTorpedoFired.value)
        self._photonTorpedoExploded: Sound = self.loadSound(bareFileName=SoundType.PhotonTorpedoExploded.value)
        self._photonTorpedoMisfire:  Sound = self.loadSound(bareFileName=SoundType.PhotonTorpedoMisfire.value)
        self._photonTorpedoMiss:     Sound = self.loadSound(bareFileName=SoundType.PhotonTorpedoMiss.value)
        self._inaccurate:            Sound = self.loadSound(bareFileName=SoundType.Inaccurate.value)
        self._klingonMove:           Sound = self.loadSound(bareFileName=SoundType.KlingonMove.value)
        self._klingonTorpedo:        Sound = self.loadSound(bareFileName=SoundType.KlingonTorpedo.value)
        self._klingonCannotFire:     Sound = self.loadSound(bareFileName=SoundType.KlingonCannotFire.value)
        self._commanderMove:         Sound = self.loadSound(bareFileName=SoundType.CommanderMove.value)
        self._commanderTorpedo:      Sound = self.loadSound(bareFileName=SoundType.CommanderTorpedo.value)
        self._commanderCannotFire:   Sound = self.loadSound(bareFileName=SoundType.CommanderCannotFire.value)
        self._superCommanderMove:    Sound = self.loadSound(bareFileName=SoundType.SuperCommanderMove.value)
        self._superCommanderTorpedo:    Sound = self.loadSound(bareFileName=SoundType.SuperCommanderTorpedo.value)
        self._superCommanderCannotFire: Sound = self.loadSound(bareFileName=SoundType.SuperCommanderCannotFire.value)

        self._warp:                  Sound = self.loadSound(bareFileName=SoundType.Warp.value)
        self._shieldHit:             Sound = self.loadSound(bareFileName=SoundType.ShieldHit.value)

        self._sounds: SoundDictionary = SoundDictionary(
            {
                SoundType.UnableToComply:        self._unableToComply,
                SoundType.Docked:                self._docked,
                SoundType.PhaserFired:           self._phaserFired,
                SoundType.PleaseRepeatRequest:   self._pleaseRepeatRequest,
                SoundType.Impulse:               self._impulse,
                SoundType.EnterpriseBlocked:     self._enterpriseBlocked,
                SoundType.PhotonTorpedoFired:    self._photonTorpedoFired,
                SoundType.PhotonTorpedoExploded: self._photonTorpedoExploded,
                SoundType.PhotonTorpedoMisfire:  self._photonTorpedoMisfire,
                SoundType.PhotonTorpedoMiss:     self._photonTorpedoMiss,
                SoundType.Inaccurate:            self._inaccurate,
                SoundType.KlingonMove:           self._klingonMove,
                SoundType.KlingonTorpedo:        self._klingonTorpedo,
                SoundType.KlingonCannotFire:     self._klingonCannotFire,
                SoundType.CommanderMove:         self._commanderMove,
                SoundType.CommanderTorpedo:      self._commanderTorpedo,
                SoundType.CommanderCannotFire:   self._commanderCannotFire,
                SoundType.SuperCommanderMove:       self._superCommanderMove,
                SoundType.SuperCommanderTorpedo:    self._superCommanderTorpedo,
                SoundType.SuperCommanderCannotFire: self._superCommanderCannotFire,

                SoundType.Warp:                  self._warp,
                SoundType.ShieldHit:             self._shieldHit
             }
        )

    def loadSound(self, bareFileName: str) -> Sound:
        """

        Args:
            bareFileName:
        """
        fqFileName: str   = LocateResources.getResourcesPath(bareFileName=bareFileName,
                                                             resourcePath=LocateResources.SOUND_RESOURCES_PATH,
                                                             packageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME)
        sound:      Sound = Sound(fqFileName)

        return sound

    def playSound(self, soundType: SoundType):
        """

        Args:
            soundType:  What we want to here
        """
        soundToPlay: Sound = self._sounds[soundType]

        soundToPlay.play(self._gameSettings.soundVolume.value)
