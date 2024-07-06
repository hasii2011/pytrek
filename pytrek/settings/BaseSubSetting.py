
from typing import cast

from codeallybasic.SingletonV3 import SingletonV3

from configparser import ConfigParser


class BaseSubSetting(metaclass=SingletonV3):

    def __init__(self, **kwargs):

        self._config: ConfigParser = cast(ConfigParser, None)

        for name, value in kwargs.items():
            protectedName: str = f'_{name}'
            if not hasattr(self, protectedName):
                raise TypeError(f"Unexpected keyword argument {protectedName}")
            setattr(self, protectedName, value)

    @property
    def configParser(self) -> ConfigParser:
        return self._config

    @configParser.setter
    def configParser(self, newValue: ConfigParser):
        # noinspection PyAttributeOutsideInit
        self._config = newValue
