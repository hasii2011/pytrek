
from unittest import TestSuite
from unittest import main as unitTestMain

from tests.ProjectTestBase import ProjectTestBase

from pytrek.guiv2.MessageConsoleSection import MessageConsoleSection


class TestMessageConsoleSection(ProjectTestBase):
    """
    """
    def setUp(self):
        super().setUp()
        self.messageConsole: MessageConsoleSection = MessageConsoleSection(left=0, bottom=0, width=0, height=0)

    def testMaxBufferedMessages(self):

        overflowCount: int = MessageConsoleSection.MAX_LINES * 2

        for x in range(overflowCount):
            self.messageConsole.displayMessage(f'Message {x}')

        self.assertEqual(MessageConsoleSection.MAX_LINES, len(self.messageConsole._statusLines), "Hmm not at limit")


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMessageConsoleSection))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
