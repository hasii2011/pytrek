from math import cos
from math import sin
from typing import cast

from logging import Logger
from logging import getLogger

from math import atan2
from math import pi
from math import radians
from math import degrees

from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.gui.gamepieces.GamePiece import GamePiece


class SmoothMotion:
    """
    A mix-in class for smooth motion
    """

    IMAGE_ROTATION: int = 90  # Image might not be lined up right, set this to offset

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._inMotion: bool = False
        """
        True if we are moving, else False
        """
        self._destinationPoint: ArcadePosition = cast(ArcadePosition, None)
        """
        The arcade game library final destination screen position if the game piece is in motion
        """

    @property
    def inMotion(self) -> bool:
        return self._inMotion

    @inMotion.setter
    def inMotion(self, newValue: bool):
        self._inMotion = newValue

    @property
    def destinationPoint(self) -> ArcadePosition:
        """
        Use for game piece motion.  This this the the ArcadePosition.
        Returns:
        """
        return self._destinationPoint

    @destinationPoint.setter
    def destinationPoint(self, destinationPoint: ArcadePosition):
        self._destinationPoint = destinationPoint

    def doMotion(self, gamePiece: GamePiece, destinationPoint: ArcadePosition, angleDiffRadians: float, actualAngleRadians: float):

        dest_x: float = destinationPoint.x
        dest_y: float = destinationPoint.y

        gamePiece.angle = degrees(actualAngleRadians) + SmoothMotion.IMAGE_ROTATION     # Convert back to degrees

        # Are we close to the correct angle? If so, move forward.
        if abs(angleDiffRadians) < pi / 4:
            self.change_x = cos(actualAngleRadians) * gamePiece.speed
            self.change_y = sin(actualAngleRadians) * gamePiece.speed

        # Fine-tune our change_x/change_y if we are really close to destinationPoint
        # point and just need to set to that location.
        traveling = False
        if abs(gamePiece.center_x - dest_x) < abs(gamePiece.change_x):
            gamePiece.center_x = dest_x
        else:
            gamePiece.center_x += self.change_x
            traveling = True

        if abs(gamePiece.center_y - dest_y) < abs(gamePiece.change_y):
            gamePiece.center_y = dest_y
        else:
            gamePiece.center_y += gamePiece.change_y
            traveling = True

        # If we have arrived, then way we are not in motion
        if not traveling:
            # self.destinationPoint = None      # Leave this set for klingon torpedo hit computation
            self._inMotion        = False
            gamePiece.angle       = 0

    def computeArcadeMotion(self, currentPoint: ArcadePosition, destinationPoint: ArcadePosition, spriteRotationAngle: float, rotationalSpeed: float):
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
        destX:  float = destinationPoint.x
        destY:  float = destinationPoint.y

        xDiff: float = destX - startX
        yDiff: float = destY - startY

        targetAngleRadians:   float = self.computeTargetAngle(xDiff, yDiff)
        actualAngleRadians:   float = radians(spriteRotationAngle - SmoothMotion.IMAGE_ROTATION)  # What angle are we at now in radians?
        rotationSpeedRadians: float = radians(rotationalSpeed)                  # How fast can we rotate?
        angleDiffRadians:     float = targetAngleRadians - actualAngleRadians        # What is the difference between what we want, and here we are?

        # Are we close enough to not need to rotate?
        clockwise: bool = cast(bool, None)
        if abs(angleDiffRadians) <= rotationSpeedRadians:
            actualAngleRadians = targetAngleRadians            # Close enough, let's set our angle to the target
        else:
            clockwise = self.rotateClockwise(angleDiffRadians=angleDiffRadians)

        actualAngleRadians = self.correctRotation(actualAngleRadians=actualAngleRadians, rotationSpeedRadians=rotationSpeedRadians,
                                                  targetAngleRadians=targetAngleRadians, clockwise=clockwise)

        return actualAngleRadians, angleDiffRadians

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

        return targetAngleRadians

    def correctRotation(self, actualAngleRadians, rotationSpeedRadians, targetAngleRadians, clockwise: bool):

        if actualAngleRadians != rotationSpeedRadians and clockwise:
            actualAngleRadians -= rotationSpeedRadians
        elif actualAngleRadians != targetAngleRadians:
            actualAngleRadians += rotationSpeedRadians

        actualAngleRadians = self.keepInRange(actualAngleRadians)

        return actualAngleRadians

    def rotateClockwise(self, angleDiffRadians: float) -> bool:
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

    def keepInRange(self, actualAngleRadians):

        # Keep in a range of 0 to 2pi
        if actualAngleRadians > 2 * pi:
            actualAngleRadians -= 2 * pi
        elif actualAngleRadians < 0:
            actualAngleRadians += 2 * pi

        return actualAngleRadians
