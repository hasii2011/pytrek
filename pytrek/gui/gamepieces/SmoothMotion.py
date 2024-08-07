
from typing import cast

from collections import namedtuple

from logging import Logger
from logging import getLogger
from logging import DEBUG

from math import atan2
from math import pi
from math import radians
from math import degrees
from math import cos
from math import sin

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.GamePiece import GamePiece

from pytrek.settings.GameSettings import GameSettings

RadianInfo = namedtuple('RadianInfo', 'actualAngleRadians, angleDiffRadians')


class SmoothMotion:
    """
    A mix-in class for smooth motion
    """
    SMOOTH_MOTION_MAX_UPDATE: int = 15

    IMAGE_ROTATION: int = 90  # Image might not be lined up right, set this to offset

    def __init__(self, imageRotation: int = IMAGE_ROTATION):

        self._smLogger: Logger = getLogger(__name__)

        self._inMotion: bool = False
        """
        True if we are moving, else False
        """
        self._destinationPoint: ArcadePoint = cast(ArcadePoint, None)
        """
        The arcade game library final destination screen position if the game piece is in motion
        """
        self._imageRotation: int = imageRotation

        self._smoothMotionCounter: int = 0
        """
        Counter that let's us know when to update the debug output
        """
        self._gameSettings:              GameSettings = GameSettings()
        self._smoothMotionDebugInterval: int          = 0

    @property
    def inMotion(self) -> bool:
        return self._inMotion

    @inMotion.setter
    def inMotion(self, newValue: bool):
        self._inMotion = newValue

    @property
    def destinationPoint(self) -> ArcadePoint:
        """
        Use for game piece motion.  This is the ArcadePoint.
        Returns:
        """
        return self._destinationPoint

    @destinationPoint.setter
    def destinationPoint(self, destinationPoint: ArcadePoint):
        self._destinationPoint = destinationPoint

    @property
    def imageRotation(self) -> int:
        return self._imageRotation

    @imageRotation.setter
    def imageRotation(self, newValue: int):
        self._imageRotation = newValue

    def doMotion(self, gamePiece: GamePiece, destinationPoint: ArcadePoint, angleDiffRadians: float, actualAngleRadians: float):

        destinationX: float = destinationPoint.x
        destinationY: float = destinationPoint.y

        gamePiece.angle = degrees(actualAngleRadians) + self.imageRotation     # Convert back to degrees

        self._smoothMotionCounter += 1
        if self._smoothMotionCounter > SmoothMotion.SMOOTH_MOTION_MAX_UPDATE:
            angleDiffDegrees:   float = degrees(angleDiffRadians)
            actualAngleDegrees: float = degrees(actualAngleRadians)

            self._smoothMotionDebugOutput(f'{gamePiece} angleDiffDegrees={angleDiffDegrees:.2f} actualAngleDegrees={actualAngleDegrees:.2f}')

        # Are we close to the correct angle? If so, move forward.
        if abs(angleDiffRadians) < pi / 4:
            gamePiece.change_x = cos(actualAngleRadians) * gamePiece.speed
            gamePiece.change_y = sin(actualAngleRadians) * gamePiece.speed

        moving: bool = self._fineTuneMotion(gamePiece=gamePiece, destinationX=destinationX, destinationY=destinationY)

        if self._smoothMotionCounter > SmoothMotion.SMOOTH_MOTION_MAX_UPDATE:
            self._smoothMotionDebugOutput(f'After: {gamePiece} ({gamePiece.center_x},{gamePiece.center_y}) destination ({destinationX},{destinationY})')
            self._smoothMotionCounter = 0

        # If we have arrived, then we are not in motion
        if not moving:
            # self.destinationPoint = None      # Leave this set for klingon torpedo hit computation
            self._inMotion  = False
            gamePiece.angle = 0

    def computeArcadeMotion(self, currentPoint: ArcadePoint, destinationPoint: ArcadePoint, spriteRotationAngle: float, rotationalSpeed: float) -> RadianInfo:
        """
        Do math to calculate how to get the sprite to the destinationPoint.
        Calculate the angle in radians between the start points
        and end points. This is the angle the player will travel.

        Args:
            currentPoint:        Sprite's current position
            destinationPoint:    Sprite's desired position
            spriteRotationAngle:    How much is sprite rotated; in radians
            rotationalSpeed:        How fast can we rotate the sprite

        Returns:
        """

        # Position the start at our current location
        startX: float = currentPoint.x
        startY: float = currentPoint.y
        destinationX:  float = destinationPoint.x
        destinationY:  float = destinationPoint.y

        xDiff: float = destinationX - startX
        yDiff: float = destinationY - startY

        targetAngleRadians:   float = self.computeTargetAngle(xDiff, yDiff)
        actualAngleRadians:   float = radians(spriteRotationAngle - self.imageRotation)  # What angle are we at now in radians?
        rotationSpeedRadians: float = radians(rotationalSpeed)                           # How fast can we rotate?
        angleDiffRadians:     float = targetAngleRadians - actualAngleRadians        # What is the difference between what we want, and here we are?

        if self._smoothMotionCounter >= SmoothMotion.SMOOTH_MOTION_MAX_UPDATE:
            self._smoothMotionDebugOutput(f'spriteRotationAngle={spriteRotationAngle:.2f} imageRotation={self.imageRotation:.2f}')

        # Are we close enough to not need to rotate?
        clockwise: bool = cast(bool, None)
        if abs(angleDiffRadians) <= rotationSpeedRadians:
            actualAngleRadians = targetAngleRadians            # Close enough, let's set our angle to the target
        else:
            clockwise = self._rotateClockwise(angleDiffRadians=angleDiffRadians)

        actualAngleRadians = self._correctRotation(actualAngleRadians=actualAngleRadians, rotationSpeedRadians=rotationSpeedRadians,
                                                   targetAngleRadians=targetAngleRadians, clockwise=clockwise)

        radianInfo: RadianInfo = RadianInfo(actualAngleRadians=actualAngleRadians, angleDiffRadians=angleDiffRadians)

        return radianInfo

    def computeTargetAngle(self, xDiff: float, yDiff: float) -> float:
        """
        Args:
            xDiff:  Difference between the 2 x coordinates
            yDiff:  Difference between the 2 y coordinates

        Returns: the angle in radians
        """

        targetAngleRadians = atan2(yDiff, xDiff)

        if targetAngleRadians < 0:
            targetAngleRadians += 2 * pi

        if self._smoothMotionCounter >= SmoothMotion.SMOOTH_MOTION_MAX_UPDATE:
            targetAngleDegrees: float = degrees(targetAngleRadians)

            self._smoothMotionDebugOutput(f'targetAngleDegrees={targetAngleDegrees:0.2f}')

        return targetAngleRadians

    def _fineTuneMotion(self, gamePiece: GamePiece, destinationX: float, destinationY: float) -> bool:
        """
        Fine-tune our change_x/change_y if we are really close to destinationPoint
        and just need to set to that location.

        Args:
            gamePiece:
            destinationX:
            destinationY:

        Returns: True if we are too far and need to continue moving
        """
        moving: bool = False
        if DEBUG:
            if self._smoothMotionCounter > SmoothMotion.SMOOTH_MOTION_MAX_UPDATE:
                self._smoothMotionDebugOutput(f'Before: {gamePiece} ({gamePiece.center_x},{gamePiece.center_y}) destination ({destinationX},{destinationY})')

        if abs(gamePiece.center_x - destinationX) < abs(gamePiece.change_x):
            gamePiece.center_x = destinationX
        else:
            gamePiece.center_x += gamePiece.change_x
            moving = True

        if abs(gamePiece.center_y - destinationY) < abs(gamePiece.change_y):
            gamePiece.center_y = destinationY
        else:
            gamePiece.center_y += gamePiece.change_y
            moving = True

        return moving

    def _correctRotation(self, actualAngleRadians, rotationSpeedRadians, targetAngleRadians, clockwise: bool):

        if actualAngleRadians != rotationSpeedRadians and clockwise:
            actualAngleRadians -= rotationSpeedRadians
        elif actualAngleRadians != targetAngleRadians:
            actualAngleRadians += rotationSpeedRadians

        actualAngleRadians = self._keepInRange(actualAngleRadians)

        return actualAngleRadians

    def _rotateClockwise(self, angleDiffRadians: float) -> bool:
        """
        Figure out if we rotate clockwise or counter-clockwise

        Args:
            angleDiffRadians:

        Returns: `True` then rotate clockwise, `False` rotate counter-clockwise
        """
        # if abs(angleDiffRadians) <= rotationSpeedRadians:
        #     # Close enough, let's set our angle to the target
        #     actualAngleRadians = targetAngleRadians
        #     clockwise = None
        if angleDiffRadians > 0 and abs(angleDiffRadians) < pi:
            clockwise = False
        elif angleDiffRadians > 0 and abs(angleDiffRadians) >= pi:
            clockwise = True
        elif angleDiffRadians < 0 and abs(angleDiffRadians) < pi:
            clockwise = True
        else:
            clockwise = False

        return clockwise

    def _keepInRange(self, actualAngleRadians):

        # Keep in a range of 0 to 2pi
        if actualAngleRadians > 2 * pi:
            actualAngleRadians -= 2 * pi
        elif actualAngleRadians < 0:
            actualAngleRadians += 2 * pi

        return actualAngleRadians

    def _smoothMotionDebugOutput(self, msg: str):

        if self._gameSettings.debugSmoothMotion is True:
            self._smoothMotionDebugInterval += 1
            if self._smoothMotionDebugInterval > self._gameSettings.debugSmoothMotionInterval:
                self._smLogger.debug(msg)
                self._smoothMotionDebugInterval = 0
