
from typing import Callable
from typing import NewType

from pytrek.model.Coordinates import Coordinates

# A method that takes the warp factor as parameter 1 and the coordinates of the new quadrant as parameter 2.
# TODO:  Figure how to tell callable function returns nothing and make mypy happy
WarpTravelCallback = NewType('WarpTravelCallback', Callable[[float, Coordinates], None])  # type: ignore
