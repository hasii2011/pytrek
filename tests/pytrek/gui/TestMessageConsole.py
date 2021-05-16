
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase

from pytrek.gui.MessageConsole import MessageConsole


class TestMessageConsole(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestMessageConsole.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()

    def setUp(self):
        self.logger:         Logger         = TestMessageConsole.clsLogger
        self.messageConsole: MessageConsole = MessageConsole()

    def tearDown(self):
        pass

    def testMaxBufferedMessages(self):

        overflowCount: int = MessageConsole.MAX_LINES * 2

        for x in range(overflowCount):
            self.messageConsole.displayMessage(f'Message {x}')

        self.assertEqual(MessageConsole.MAX_LINES, len(self.messageConsole._statusLines), "Hmm not at limit")


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMessageConsole))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
