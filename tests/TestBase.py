
from typing import cast


from hasiihelper.UnitTestBase import UnitTestBase


from hasiihelper.Singleton import Singleton

from pytrek.GameState import GameState

from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.futures.EventEngine import EventEngine
from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Galaxy import Galaxy

from pytrek.settings.GameSettings import GameSettings


class TestBase(UnitTestBase):
    # noinspection SpellCheckingInspection
    RESOURCES_TEST_CLASSES_PACKAGE_NAME: str = 'tests.resources.testclass'

    """
    A base unit test class to initialize some logging stuff we need
    """

    @classmethod
    def resetSingletons(cls):
        """
        Force stateful singletons to re-initialize
        """
        GameSettings.__instance__ = cast(Singleton, None)
        Intelligence.__instance__ = cast(Singleton, None)
        GameState.__instance__    = cast(Singleton, None)
        Galaxy.__instance__       = cast(Singleton, None)
        GameEngine.__instance__   = cast(Singleton, None)
        EventEngine.__instance__  = cast(Singleton, None)
        Devices.__instance__      = cast(Singleton, None)
        Galaxy.__instance__       = cast(Singleton, None)
        GalaxyMediator.__instance__   = cast(Singleton, None)
        QuadrantMediator.__instance__ = cast(Singleton, None)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
