
from typing import cast

from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from pytrek.Singleton import Singleton

from pytrek.engine.GameType import GameType
from pytrek.engine.PlayerType import PlayerType
from pytrek.settings.DebugSettings import DebugSettings

from pytrek.settings.FactorsSettings import FactorsSettings
from pytrek.settings.GameLevelSettings import GameLevelSettings
from pytrek.settings.LimitsSettings import LimitsSettings
from pytrek.settings.PowerSettings import PowerSettings
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SoundVolume import SoundVolume
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds
from pytrek.settings.TorpedoSpeedSettings import TorpedoSpeedSettings


class GameSettings(Singleton):

    def init(self):

        self.logger: Logger = getLogger(__name__)

        self._config: ConfigParser = cast(ConfigParser, None)    # initialized when empty preferences created

        self._settingsCommon: SettingsCommon       = SettingsCommon()
        self._limits:         LimitsSettings       = LimitsSettings()
        self._power:          PowerSettings        = PowerSettings()
        self._gameLevel:      GameLevelSettings    = GameLevelSettings()
        self._factors:        FactorsSettings      = FactorsSettings()
        self._debug:          DebugSettings        = DebugSettings()
        self._torpedoSpeeds:  TorpedoSpeedSettings = TorpedoSpeedSettings()

        self._createEmptySettings()
        self._loadSettings()

    @property
    def maximumStars(self) -> int:
        return self._limits.maximumStars

    @property
    def minimumStarBases(self) -> int:
        return self._limits.minimumStarBases

    @property
    def maximumStarBases(self) -> int:
        return self._limits.maximumStarBases

    @property
    def maximumPlanets(self) -> int:
        return self._limits.maximumPlanets

    @property
    def initialEnergyLevel(self) -> int:
        return self._power.initialEnergyLevel

    @property
    def initialShieldEnergy(self) -> int:
        return self._power.initialShieldEnergy

    @property
    def initialTorpedoCount(self) -> int:
        return self._power.initialTorpedoCount

    @property
    def minimumImpulseEnergy(self) -> int:
        return self._power.minimumImpulseEnergy

    @property
    def playerType(self) -> PlayerType:
        return self._gameLevel.playerType

    @playerType.setter
    def playerType(self, newValue: PlayerType):
        self._gameLevel.playerType = newValue

    @property
    def gameType(self) -> GameType:
        return self._gameLevel.gameType

    @gameType.setter
    def gameType(self, newValue: GameType):
        self._gameLevel.gameType = newValue

    @property
    def soundVolume(self) -> SoundVolume:
        return self._gameLevel.soundVolume

    @soundVolume.setter
    def soundVolume(self, newValue: SoundVolume):
        self._gameLevel.soundVolume = newValue

    @property
    def gameLengthFactor(self) -> float:
        return self._factors.gameLengthFactor

    @property
    def starBaseExtender(self) -> float:
        return self._factors.starBaseExtender

    @property
    def starBaseMultiplier(self) -> float:
        return self._factors.starBaseMultiplier

    @property
    def minKlingonFiringInterval(self) -> int:
        return self._factors.minKlingonFiringInterval

    @property
    def maxKlingonFiringInterval(self) -> int:
        return self._factors.maxKlingonFiringInterval

    @property
    def minCommanderFiringInterval(self) -> int:
        return self._factors.minCommanderFiringInterval

    @property
    def maxCommanderFiringInterval(self) -> int:
        return self._factors.maxCommanderFiringInterval

    @property
    def minSuperCommanderFiringInterval(self) -> int:
        return self._factors.minSuperCommanderFiringInterval

    @property
    def maxSuperCommanderFiringInterval(self) -> int:
        return self._factors.maxSuperCommanderFiringInterval

    @property
    def minCommanderMoveInterval(self) -> int:
        return self._factors.minCommanderMoveInterval

    @property
    def maxCommanderMoveInterval(self) -> int:
        return self._factors.maxCommanderMoveInterval

    @property
    def minSuperCommanderMoveInterval(self) -> int:
        return self._factors.minSuperCommanderMoveInterval

    @property
    def maxSuperCommanderMoveInterval(self) -> int:
        return self._factors.maxSuperCommanderMoveInterval

    @property
    def minKlingonMoveInterval(self) -> int:
        return self._factors.minKlingonMoveInterval

    @property
    def maxKlingonMoveInterval(self) -> int:
        return self._factors.maxKlingonMoveInterval

    @property
    def basicMissDisplayInterval(self) -> int:
        return self._factors.basicMissDisplayInterval

    @property
    def photonTorpedoMisfireRate(self) -> float:
        return self._factors.photonTorpedoMisfireRate

    @property
    def noviceTorpedoSpeeds(self) -> TorpedoSpeeds:
        return self._torpedoSpeeds.noviceTorpedoSpeeds

    @property
    def fairTorpedoSpeeds(self) -> TorpedoSpeeds:
        return self._torpedoSpeeds.fairTorpedoSpeeds

    @property
    def goodTorpedoSpeeds(self) -> TorpedoSpeeds:
        return self._torpedoSpeeds.goodTorpedoSpeeds

    @property
    def expertTorpedoSpeeds(self) -> TorpedoSpeeds:
        return self._torpedoSpeeds.expertTorpedoSpeeds

    @property
    def emeritusTorpedoSpeeds(self) -> TorpedoSpeeds:
        return self._torpedoSpeeds.emeritusTorpedoSpeeds

    @property
    def debugAddKlingons(self) -> bool:
        return self._debug.debugAddKlingons

    @debugAddKlingons.setter
    def debugAddKlingons(self, newValue: bool):
        self._debug.debugAddKlingons = newValue

    @property
    def debugKlingonCount(self) -> int:
        return self._debug.debugKlingonCount

    @debugKlingonCount.setter
    def debugKlingonCount(self, newValue: int):
        self._debug.debugKlingonCount = newValue

    @property
    def debugAddCommanders(self) -> bool:
        return self._debug.debugAddCommanders

    @property
    def debugCommanderCount(self) -> int:
        return self._debug.debugCommanderCount

    @property
    def debugAddSuperCommanders(self) -> bool:
        return self._debug.debugAddSuperCommanders

    @property
    def debugSuperCommanderCount(self) -> int:
        return self._debug.debugSuperCommanderCount

    @property
    def debugPrintKlingonPlacement(self) -> bool:
        return self._debug.debugPrintKlingonPlacement

    @debugPrintKlingonPlacement.setter
    def debugPrintKlingonPlacement(self, newValue: bool):
        self._debug.debugPrintKlingonPlacement = newValue

    @property
    def debugCollectKlingonQuadrantCoordinates(self) -> bool:
        return self._debug.debugCollectKlingonQuadrantCoordinates

    @debugCollectKlingonQuadrantCoordinates.setter
    def debugCollectKlingonQuadrantCoordinates(self, newValue: bool):
        self._debug.debugCollectKlingonQuadrantCoordinates = newValue

    @property
    def debugAnnounceQuadrantCreation(self) -> bool:
        return self._debug.debugAnnounceQuadrantCreation

    @debugAnnounceQuadrantCreation.setter
    def debugAnnounceQuadrantCreation(self, newValue: bool):
        self._debug.debugAnnounceQuadrantCreation = newValue

    @property
    def debugAddPlanet(self) -> bool:
        return self._debug.debugAddPlanet

    @debugAddPlanet.setter
    def debugAddPlanet(self, newValue: bool):
        self._debug.debugAddPlanet = newValue

    @property
    def debugNoKlingons(self) -> bool:
        return self._debug.debugNoKlingons

    @debugNoKlingons.setter
    def debugNoKlingons(self, newValue: bool):
        self._debug.debugNoKlingons = newValue

    @property
    def debugNoCommanders(self) -> bool:
        return self._debug.debugNoCommanders

    @debugNoCommanders.setter
    def debugNoCommanders(self, newValue: bool):
        self._debug.debugNoCommanders = newValue

    @property
    def debugNoSuperCommanders(self) -> bool:
        return self._debug.debugNoSuperCommanders

    @debugNoSuperCommanders.setter
    def debugNoSuperCommanders(self, newValue: bool):
        self._debug.debugNoSuperCommanders = newValue

    def _createEmptySettings(self):

        self._config: ConfigParser = ConfigParser()

        self._settingsCommon.configParser = self._config
        self._limits.configParser         = self._config
        self._power.configParser          = self._config
        self._gameLevel.configParser      = self._config
        self._factors.configParser        = self._config
        self._debug.configParser          = self._config
        self._torpedoSpeeds.configParser  = self._config

    def _loadSettings(self):
        """
        Load settings from settings file
        """
        # Make sure that the settings file exists
        # noinspection PyUnusedLocal
        try:
            f = open(SettingsCommon.getSettingsLocation(), "r")
            f.close()
        except (ValueError, Exception) as e:
            try:
                f = open(SettingsCommon.getSettingsLocation(), "w")
                f.write("")
                f.close()
                self.logger.warning(f'Game Settings File file re-created')
            except (ValueError, Exception) as e:
                self.logger.error(f"Error: {e}")
                return

        # Read data
        self._config.read(SettingsCommon.getSettingsLocation())

        self._limits.addMissingSettings()
        self._power.addMissingSettings()
        self._gameLevel.addMissingSettings()
        self._factors.addMissingSettings()
        self._debug.addMissingSettings()
        self._torpedoSpeeds.addMissingSettings()
