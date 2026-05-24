
from codeallybasic.UnitTestBase import UnitTestBase

from src.pytrek.GameState import GameState

from src.pytrek.engine.GameEngine import GameEngine
from src.pytrek.engine.Intelligence import Intelligence
from src.pytrek.engine.devices import DeviceManager
from src.pytrek.engine.futures.EventEngine import EventEngine

from src.pytrek.mediators.GalaxyMediator import GalaxyMediator
from src.pytrek.mediators.QuadrantMediator import QuadrantMediator

from src.pytrek.model import Galaxy

from src.pytrek.settings.GameSettings import GameSettings


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
        DeviceManager._instances    = {}
