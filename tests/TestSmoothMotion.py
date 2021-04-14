
from logging import Logger
from logging import getLogger

from math import radians
from math import degrees

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.gui.gamepieces.GamePiece import GamePiece
from tests.TestBase import TestBase


from pytrek.gui.gamepieces.SmoothMotion import SmoothMotion


class TestSmoothMotion(TestBase):
    """
    """
    TEST_ROTATIONAL_SPEED: int = 5

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestSmoothMotion.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:       Logger       = TestSmoothMotion.clsLogger
        self.smoothMotion: SmoothMotion = SmoothMotion()

    def tearDown(self):
        pass

    def testDoMotion(self):

        currentPosition:     ArcadePosition = ArcadePosition(x=0, y=0)
        destinationPosition: ArcadePosition = ArcadePosition(x=0, y=500)

        self.smoothMotion.computeArcadeMotion(currentPoint=currentPosition, destinationPoint=destinationPosition,
                                              spriteRotationAngle=0,
                                              rotationalSpeed=TestSmoothMotion.TEST_ROTATIONAL_SPEED)

        mockSprite: MagicMock(spec=GamePiece)

    def testComputeTargetAngle(self):

        self._checkAngle(xDiff=0,   yDiff=500, expectedAngle=90.0, failMessage='Bad 90 degree computation')
        self._checkAngle(xDiff=500, yDiff=0,   expectedAngle=0.0,  failMessage='Bad 0 degree computation')
        self._checkAngle(xDiff=500, yDiff=500, expectedAngle=45.0, failMessage='Bad 45 degree computation')

        self._checkAngle(xDiff=0, yDiff=-500,    expectedAngle=270.0, failMessage='Bad 270 degree computation')
        self._checkAngle(xDiff=-500, yDiff=0,    expectedAngle=180.0, failMessage='Bad 180 degree computation')
        self._checkAngle(xDiff=-500, yDiff=-500, expectedAngle=225.0, failMessage='Bad 225 degree computation')

        rotationSpeedRadians: float = radians(5)                  # How fast can we rotate?
        self.logger.info(f'{rotationSpeedRadians=}')

    def testRotateClockwise(self):

        spriteRotationAngle: float = radians(0)
        self._checkRotateClockWise(spriteRotationAngle=spriteRotationAngle, xDiff=500, yDiff=500, expectedAnswer=False)

        spriteRotationAngle = radians(180)
        self._checkRotateClockWise(spriteRotationAngle=spriteRotationAngle, xDiff=-500, yDiff=-500, expectedAnswer=True)

    def _checkAngle(self, xDiff: float, yDiff: float, expectedAngle: float, failMessage: str):

        targetAngle:  float = self.smoothMotion.computeTargetAngle(yDiff=yDiff, xDiff=xDiff)
        angleDegrees: float = degrees(targetAngle)

        self.logger.info(f'Radians: {targetAngle=} {angleDegrees=}')
        self.assertEqual(expectedAngle, angleDegrees, failMessage)

    def _checkRotateClockWise(self, spriteRotationAngle: float, xDiff: float, yDiff: float, expectedAnswer: bool):

        rotationSpeedRadians: float = radians(TestSmoothMotion.TEST_ROTATIONAL_SPEED)
        targetAngleRadians:   float = self.smoothMotion.computeTargetAngle(xDiff=xDiff, yDiff=yDiff)

        actualAngleRadians:   float = radians(spriteRotationAngle - SmoothMotion.IMAGE_ROTATION)  # What angle are we at now in radians?

        angleDiffRadians:     float = targetAngleRadians - actualAngleRadians        # What is the difference between what we want, and where we are?

        self.logger.info(f'{angleDiffRadians=}')

        rotateClockwise: bool = self.smoothMotion.rotateClockwise(angleDiffRadians=angleDiffRadians)

        self.logger.info(f'{rotateClockwise=}')

        self.assertEqual(expectedAnswer, rotateClockwise, 'Fail')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestSmoothMotion))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
