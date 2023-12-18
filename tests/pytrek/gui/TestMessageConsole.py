
from unittest import TestSuite
from unittest import main as unitTestMain

from tests.ProjectTestBase import ProjectTestBase

from pytrek.gui.MessageConsole import MessageConsole


class TestMessageConsole(ProjectTestBase):
    """
    """
    def setUp(self):
        super().setUp()
        self.messageConsole: MessageConsole = MessageConsole()

    def testMaxBufferedMessages(self):

        overflowCount: int = MessageConsole.MAX_LINES * 2

        for x in range(overflowCount):
            self.messageConsole.displayMessage(f'Message {x}')

        self.assertEqual(MessageConsole.MAX_LINES, len(self.messageConsole._statusLines), "Hmm not at limit")


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMessageConsole))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
