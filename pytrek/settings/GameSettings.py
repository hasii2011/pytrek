
from typing import cast

from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from pytrek.Singleton import Singleton

from pytrek.engine.GameType import GameType
from pytrek.engine.PlayerType import PlayerType

from pytrek.settings.FactorsSettings import FactorsSettings
from pytrek.settings.GameLevelSettings import GameLevelSettings
from pytrek.settings.LimitsSettings import LimitsSettings
from pytrek.settings.PowerSettings import PowerSettings
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SoundVolume import SoundVolume
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds
from pytrek.settings.TorpedoSpeedSettings import TorpedoSpeedSettings
from pytrek.settings.DebugSettings import DebugSettings
from pytrek.settings.DeveloperSettings import DeveloperSettings


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
        self._developer:      DeveloperSettings    = DeveloperSettings()

        self._createEmptySettings()
        self._loadSettings()

        self.logger.info(f'Game Settings singleton initialized')

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
    def defaultFullShields(self) -> int:
        return self._limits.defaultFullShields

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
    def defaultWarpFactor(self) -> int:
        return self._power.defaultWarpFactor

    @property
    def phaserFactor(self) -> float:
        return self._power.phaserFactor

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
    def phaserBurstToTerminate(self) -> float:
        return self._factors.phaserBurstToTerminate

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
        return self._debug.addKlingons

    @debugAddKlingons.setter
    def debugAddKlingons(self, newValue: bool):
        self._debug.addKlingons = newValue

    @property
    def debugKlingonCount(self) -> int:
        return self._debug.klingonCount

    @debugKlingonCount.setter
    def debugKlingonCount(self, newValue: int):
        self._debug.klingonCount = newValue

    @property
    def debugAddCommanders(self) -> bool:
        return self._debug.addCommanders

    @property
    def debugCommanderCount(self) -> int:
        return self._debug.commanderCount

    @property
    def debugAddSuperCommanders(self) -> bool:
        return self._debug.addSuperCommanders

    @property
    def debugSuperCommanderCount(self) -> int:
        return self._debug.superCommanderCount

    @property
    def debugPrintKlingonPlacement(self) -> bool:
        return self._debug.printKlingonPlacement

    @debugPrintKlingonPlacement.setter
    def debugPrintKlingonPlacement(self, newValue: bool):
        self._debug.printKlingonPlacement = newValue

    @property
    def debugCollectKlingonQuadrantCoordinates(self) -> bool:
        return self._debug.collectKlingonQuadrantCoordinates

    @debugCollectKlingonQuadrantCoordinates.setter
    def debugCollectKlingonQuadrantCoordinates(self, newValue: bool):
        self._debug.collectKlingonQuadrantCoordinates = newValue

    @property
    def debugAnnounceQuadrantCreation(self) -> bool:
        return self._debug.announceQuadrantCreation

    @debugAnnounceQuadrantCreation.setter
    def debugAnnounceQuadrantCreation(self, newValue: bool):
        self._debug.announceQuadrantCreation = newValue

    @property
    def debugAddPlanet(self) -> bool:
        return self._debug.addPlanet

    @debugAddPlanet.setter
    def debugAddPlanet(self, newValue: bool):
        self._debug.addPlanet = newValue

    @property
    def debugAddStarBase(self) -> bool:
        return self._debug.addStarBase

    @debugAddStarBase.setter
    def debugAddStarBase(self, newValue: bool):
        self._debug.addStarBase = newValue

    @property
    def debugNoKlingons(self) -> bool:
        return self._debug.noKlingons

    @debugNoKlingons.setter
    def debugNoKlingons(self, newValue: bool):
        self._debug.noKlingons = newValue

    @property
    def debugNoCommanders(self) -> bool:
        return self._debug.noCommanders

    @debugNoCommanders.setter
    def debugNoCommanders(self, newValue: bool):
        self._debug.noCommanders = newValue

    @property
    def debugNoSuperCommanders(self) -> bool:
        return self._debug.noSuperCommanders

    @debugNoSuperCommanders.setter
    def debugNoSuperCommanders(self, newValue: bool):
        self._debug.noSuperCommanders = newValue

    @property
    def debugConsoleShowInternals(self) -> bool:
        return self._debug.consoleShowInternals

    @debugConsoleShowInternals.setter
    def debugConsoleShowInternals(self, newValue: bool):
        self._debug.consoleShowInternals = newValue

    @property
    def maxStarbaseSearches(self) -> int:
        return self._developer.maxStarbaseSearches

    @maxStarbaseSearches.setter
    def maxStarbaseSearches(self, newValue: int):
        self._developer.maxStarbaseSearches = newValue

    @property
    def maxCommanderSearches(self) -> int:
        return self._developer.maxCommanderSearches

    @maxCommanderSearches.setter
    def maxCommanderSearches(self, newValue: int):
        self._developer.maxCommanderSearches = newValue

    def _createEmptySettings(self):

        self._config: ConfigParser = ConfigParser()

        self._settingsCommon.configParser = self._config
        self._limits.configParser         = self._config
        self._power.configParser          = self._config
        self._gameLevel.configParser      = self._config
        self._factors.configParser        = self._config
        self._debug.configParser          = self._config
        self._torpedoSpeeds.configParser  = self._config
        self._developer.configParser      = self._config

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
        self._developer.addMissingSettings()
