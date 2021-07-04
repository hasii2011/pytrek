
from logging import Logger
from logging import getLogger

from pytrek.engine.PlayerType import PlayerType

from pytrek.settings.BaseSubSetting import BaseSubSetting
from pytrek.settings.SettingsCommon import SettingsCommon
from pytrek.settings.SettingsCommon import SettingsNameValues
from pytrek.settings.TorpedoSpeeds import TorpedoSpeeds


class TorpedoSpeedSettings(BaseSubSetting):

    SPEED_SECTION: str = 'TorpedoSpeeds'

    NOVICE_PLAYER:   str = PlayerType.Novice.name
    FAIR_PLAYER:     str = PlayerType.Fair.name
    GOOD_PLAYER:     str = PlayerType.Good.name
    EXPERT_PLAYER:   str = PlayerType.Expert.name
    EMERITUS_PLAYER: str = PlayerType.Emeritus.name
    #
    # The specific value setting is a comma delimited string
    # for each torpedo type of the form:
    #
    #  enterprise,klingon,commander,super commander
    #
    # -1 value used because super commander are not generated for Novice or Fair players
    #
    SPEED_SETTINGS:  SettingsNameValues = SettingsNameValues({
        NOVICE_PLAYER:   '5,2,2,-1',
        FAIR_PLAYER:     '4,2,2,-1',
        GOOD_PLAYER:     '3,2,3,4',
        EXPERT_PLAYER:   '2,2,4,4',
        EMERITUS_PLAYER: '1,2,5,5',
    })

    def init(self, *args, **kwds):
        """
        This is a singleton based on the inheritance hierarchy
        """
        self.logger: Logger = getLogger(__name__)

        BaseSubSetting.init(self, *args, **kwds)

        self._settingsCommon: SettingsCommon = SettingsCommon(self._config)

    def addMissingSettings(self):
        self._settingsCommon.addMissingSettings(sectionName=TorpedoSpeedSettings.SPEED_SECTION, nameValues=TorpedoSpeedSettings.SPEED_SETTINGS)

    @property
    def noviceTorpedoSpeeds(self) -> TorpedoSpeeds:
        speedStr: str           = self._config.get(TorpedoSpeedSettings.SPEED_SECTION, TorpedoSpeedSettings.NOVICE_PLAYER)
        tp:       TorpedoSpeeds = TorpedoSpeeds.toTorpedoSpeed(speedStr)
        tp.playerType = PlayerType.Novice
        return tp

    @property
    def fairTorpedoSpeeds(self) -> TorpedoSpeeds:
        speedStr: str           = self._config.get(TorpedoSpeedSettings.SPEED_SECTION, TorpedoSpeedSettings.FAIR_PLAYER)
        tp:       TorpedoSpeeds = TorpedoSpeeds.toTorpedoSpeed(speedStr)
        tp.playerType = PlayerType.Fair

        return tp

    @property
    def goodTorpedoSpeeds(self) -> TorpedoSpeeds:
        speedStr: str           = self._config.get(TorpedoSpeedSettings.SPEED_SECTION, TorpedoSpeedSettings.GOOD_PLAYER)
        tp:       TorpedoSpeeds = TorpedoSpeeds.toTorpedoSpeed(speedStr)
        tp.playerType = PlayerType.Good

        return tp

    @property
    def expertTorpedoSpeeds(self) -> TorpedoSpeeds:
        speedStr: str           = self._config.get(TorpedoSpeedSettings.SPEED_SECTION, TorpedoSpeedSettings.EXPERT_PLAYER)
        tp:       TorpedoSpeeds = TorpedoSpeeds.toTorpedoSpeed(speedStr)

        tp.playerType = PlayerType.Expert

        return tp

    @property
    def emeritusTorpedoSpeeds(self) -> TorpedoSpeeds:
        speedStr: str           = self._config.get(TorpedoSpeedSettings.SPEED_SECTION, TorpedoSpeedSettings.EMERITUS_PLAYER)
        tp:       TorpedoSpeeds = TorpedoSpeeds.toTorpedoSpeed(speedStr)

        tp.playerType = PlayerType.Emeritus

        return tp
