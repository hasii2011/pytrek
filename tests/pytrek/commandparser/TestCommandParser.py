
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pytrek.commandparser.CommandParser import CommandParser
from pytrek.commandparser.CommandType import CommandType
from pytrek.commandparser.ManualMoveData import ManualMoveData
from pytrek.commandparser.ParsedCommand import ParsedCommand

from pytrek.commandparser.InvalidCommandException import InvalidCommandException
from pytrek.commandparser.InvalidCommandValueException import InvalidCommandValueException
from pytrek.model.Coordinates import Coordinates

KeyStrokes = NewType('KeyStrokes', List[int])


class TestCommandParser(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 27 July 2024
    """
    clsLogger: Logger

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        TestCommandParser.clsLogger = getLogger(__name__)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testRestCommand(self):

        parseCommand: ParsedCommand = self._processCommand('rest 6')

        self.assertEqual(CommandType.Rest, parseCommand.commandType, 'Invalid command')
        self.assertEqual(6, parseCommand.restInterval, 'Invalid interval')

    def testChartCommand(self):

        parseCommand: ParsedCommand = self._processCommand('chart')

        self.assertEqual(CommandType.Chart, parseCommand.commandType, 'Invalid chart command')

    def testLongRangeScanCommand(self):
        parseCommand: ParsedCommand = self._processCommand('L')

        self.assertEqual(CommandType.LongRangeScan, parseCommand.commandType, 'Invalid long range scan command')

    def testDamagesCommand(self):
        parseCommand: ParsedCommand = self._processCommand('da')

        self.assertEqual(CommandType.Damages, parseCommand.commandType, 'Invalid damages command')

    def testPhasersCommand(self):
        parseCommand: ParsedCommand = self._processCommand('phasers 250')

        self.assertEqual(CommandType.Phasers, parseCommand.commandType, 'Invalid command')
        self.assertEqual(250, parseCommand.phaserAmountToFire, 'Invalid phaser power')

    def testPhotonsCommand(self):

        parseCommand: ParsedCommand = self._processCommand('photons 3')

        self.assertEqual(CommandType.Photons, parseCommand.commandType, 'Invalid photon command')
        self.assertEqual(3, parseCommand.numberOfPhotonTorpedoesToFire, 'Invalid photon count')

    def testWarpCommand(self):
        parseCommand: ParsedCommand = self._processCommand('warp 3')

        self.assertEqual(CommandType.Warp, parseCommand.commandType, 'Should be a warp command')
        self.assertEqual(3, parseCommand.warpFactor, 'Did not get a value')

    def testInvalidCommand(self):
        self.assertRaises(InvalidCommandException, lambda: self._processCommand('BadCommand'))

    def testInvalidCommandValue(self):
        self.assertRaises(InvalidCommandValueException, lambda: self._processCommand('rest q'))

    def testMoveManualPositiveDisplacement(self):
        parsedCommand: ParsedCommand = self._processCommand('MovE manual 5 5')

        self.assertEqual(CommandType.Move, parsedCommand.commandType, 'Should be a `move` command')

        expectedMoveData: ManualMoveData = ManualMoveData(deltaX=5, deltaY=5)

        self.assertEqual(expectedMoveData, parsedCommand.manualMoveData, '')
        self.assertTrue(parsedCommand.manualMove, 'Should be a manual move')

    def testSimplestManualMove(self):
        parsedCommand: ParsedCommand = self._processCommand('m m .1')

        self.assertEqual(CommandType.Move, parsedCommand.commandType, 'Should be a `move` command')
        self.assertTrue(parsedCommand.manualMove, 'Should be a manual move')

    def testSimplestNegativeManualMove(self):
        parsedCommand: ParsedCommand = self._processCommand('m m -.1')

        self.assertEqual(CommandType.Move, parsedCommand.commandType, 'Should be a `move` command')
        self.assertTrue(parsedCommand.manualMove, 'Should be a manual move')

    def testMoveAutomaticInQuadrant(self):
        parsedCommand: ParsedCommand = self._processCommand('move auto 4 4')

        expectedSectorCoordinates: Coordinates = Coordinates(x=4, y=4)

        self.assertEqual(expectedSectorCoordinates, parsedCommand.automaticMoveData.sectorCoordinates, 'Invalid quadrant move')

    def testMoveAutomaticToQuadrant(self):

        parsedCommand: ParsedCommand = self._processCommand('move automatic 3 7 5 8')

        expectedQuadrantCoordinates: Coordinates = Coordinates(x=3, y=7)
        expectedSectorCoordinates:   Coordinates = Coordinates(x=5, y=8)

        self.assertEqual(expectedQuadrantCoordinates, parsedCommand.automaticMoveData.quadrantCoordinates, 'Invalid Quadrant')
        self.assertEqual(expectedSectorCoordinates,   parsedCommand.automaticMoveData.sectorCoordinates, 'Invalid Sector')

    def _processCommand(self, commandStr: str) -> ParsedCommand:

        commandParser: CommandParser = CommandParser()
        return commandParser.parseCommand(commandStr)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestCommandParser))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
