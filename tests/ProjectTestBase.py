
from codeallybasic.UnitTestBase import UnitTestBase

from pytrek.GameState import GameState

from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence
from pytrek.engine.devices.Devices import Devices
from pytrek.engine.futures.EventEngine import EventEngine

from pytrek.mediators.GalaxyMediator import GalaxyMediator
from pytrek.mediators.QuadrantMediator import QuadrantMediator

from pytrek.model.Galaxy import Galaxy

from pytrek.settings.GameSettings import GameSettings


class ProjectTestBase(UnitTestBase):

    RESOURCES_TEST_DATA_PACKAGE_NAME: str = f'{UnitTestBase.RESOURCES_PACKAGE_NAME}.testdata'
    """
    A project base unit test class to define additional items we need
    """
    @classmethod
    def setUpClass(cls):
        """"""
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @classmethod
    def resetSingletons(cls):
        """
        Force stateful singletons to re-initialize
        """
        GameSettings._instances     = {}
        GameState._instances        = {}
        GalaxyMediator._instances   = {}
        QuadrantMediator._instances = {}
        EventEngine._instances      = {}
        Galaxy._instances           = {}
        Intelligence._instances     = {}
        GameEngine._instances       = {}
        Devices._instances          = {}
