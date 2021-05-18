
from logging import Logger
from logging import getLogger

from pytrek.engine.GameType import GameType
from pytrek.engine.PlayerType import PlayerType

from pytrek.settings.BaseSubSetting import BaseSubSetting
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SettingsCommon import SettingsNameValues


class GameLevelSettings(BaseSubSetting):

    GAME_LEVEL_SECTION: str = 'GameLevel'

    PLAYER_TYPE: str = 'player_type'
    GAME_TYPE:   str = 'game_type'

    GAME_LEVEL_SETTINGS:  SettingsNameValues = {
        PLAYER_TYPE: PlayerType.Expert.name,
        GAME_TYPE:   GameType.Long.name
    }

    def init(self, *args, **kwds):
        """
        This is a singleton based on the inheritance hierarchy
        """
        self.logger: Logger = getLogger(__name__)

        BaseSubSetting.init(self, *args, **kwds)

        self._settingsCommon: SettingsCommon = SettingsCommon(self._config)

    def addMissingSettings(self):
        self._settingsCommon.addMissingSettings(sectionName=GameLevelSettings.GAME_LEVEL_SECTION, nameValues=GameLevelSettings.GAME_LEVEL_SETTINGS)

    @property
    def playerType(self) -> PlayerType:

        playerTypeStr: str = self._config.get(GameLevelSettings.GAME_LEVEL_SECTION, GameLevelSettings.PLAYER_TYPE)

        return PlayerType[playerTypeStr]

    @playerType.setter
    def playerType(self, newValue: PlayerType):

        self._config.set(GameLevelSettings.GAME_LEVEL_SECTION, GameLevelSettings.PLAYER_TYPE, newValue.name)
        self._settingsCommon.saveSettings()

    @property
    def gameType(self) -> GameType:

        gameTypeStr: str = self._config.get(GameLevelSettings.GAME_LEVEL_SECTION, GameLevelSettings.GAME_TYPE)

        return GameType[gameTypeStr]

    @gameType.setter
    def gameType(self, newValue: GameType):
        self._config.set(GameLevelSettings.GAME_LEVEL_SECTION, GameLevelSettings.GAME_TYPE, newValue.name)
        self._settingsCommon.saveSettings()
