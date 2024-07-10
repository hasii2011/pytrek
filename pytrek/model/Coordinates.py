
from dataclasses import dataclass
from typing import List

from pytrek.Constants import MAXIMUM_COORDINATE
from pytrek.Constants import MINIMUM_COORDINATE
from pytrek.engine.Direction import Direction


@dataclass
class Coordinates:
    """
    Base class for sector and quadrant coordinates
    """
    x: int = 0
    y: int = 0

    def valid(self) -> bool:
        """
        Assumes that the Galaxy and quadrants are exactly sized

        Returns:    The min/max values should match what is in Constants
        """
        ans: bool = False
        # if self.x >= 0 and self.x <= 9 and self.y >=0 and self.y <= 9:
        if MINIMUM_COORDINATE <= self.x <= MAXIMUM_COORDINATE and MINIMUM_COORDINATE <= self.y <= MAXIMUM_COORDINATE:
            ans = True

        return ans

    def newCoordinates(self, newDirection: Direction) -> "Coordinates":
        """
        Duck typing is weird

        Please do `.valid` after calling this method

        Args:
            newDirection: How to generate coordinates

        Returns:  New potentially invalid coordinates

        """
        newCoordinates: Coordinates = Coordinates(self.x, self.y)

        if newDirection == Direction.North:
            newCoordinates.y -= 1
        elif newDirection == Direction.South:
            newCoordinates.y += 1
        elif newDirection == Direction.East:
            newCoordinates.x += 1
        elif newDirection == Direction.West:
            newCoordinates.x -= 1
        elif newDirection == Direction.NorthEast:
            newCoordinates.x += 1
            newCoordinates.y -= 1
        elif newDirection == Direction.NorthWest:
            newCoordinates.x -= 1
            newCoordinates.y -= 1
        elif newDirection == Direction.SouthEast:
            newCoordinates.x += 1
            newCoordinates.y += 1
        elif newDirection == Direction.SouthWest:
            newCoordinates.x -= 1
            newCoordinates.y += 1
        else:
            assert False

        return newCoordinates

    def toJson(self):

        return {
            'x': self.x,
            'y': self.y,
        }

    @classmethod
    def toCoordinates(cls, values: str) -> "Coordinates":
        """
        Assumes the string is in the format x,y;  e.g. '0,0' or '5,5'

        Args:
            values: The string representation

        Returns:  A Coordinate object
        """
        valueList: List[str] = values.split(',')

        x: int = int(valueList[0])
        y: int = int(valueList[1])

        coordinates: Coordinates = Coordinates(x=x, y=y)
        if coordinates.valid() is False:
            coordinates = Coordinates(x=0, y=0)

        return coordinates

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __eq__(self, other) -> bool:
        """"""
        if isinstance(other, Coordinates):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            return False
