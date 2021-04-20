
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


class GameSettings(Singleton):

    def init(self):

        self.logger: Logger = getLogger(__name__)

        self._config: ConfigParser = cast(ConfigParser, None)    # initialized when empty preferences created

        self._settingsCommon: SettingsCommon    = SettingsCommon()
        self._limits:         LimitsSettings    = LimitsSettings()
        self._power:          PowerSettings     = PowerSettings()
        self._gameLevel:      GameLevelSettings = GameLevelSettings()
        self._factors:        FactorsSettings   = FactorsSettings()

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
    def gameLengthFactor(self) -> float:
        return self._factors.gameLengthFactor

    @property
    def starBaseExtender(self) -> float:
        return self._factors.starBaseExtender

    @property
    def starBaseMultiplier(self) -> float:
        return self._factors.starBaseMultiplier

    def _createEmptySettings(self):

        self._config: ConfigParser = ConfigParser()

        self._settingsCommon.configParser = self._config
        self._limits.configParser         = self._config
        self._power.configParser          = self._config
        self._gameLevel.configParser      = self._config
        self._factors.configParser        = self._config

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
