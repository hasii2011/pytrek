
from typing import Callable
from typing import List
from typing import NewType

from arcade import Texture

from pytrek.model.Coordinates import Coordinates

# A method that takes the warp factor as parameter 1 and the coordinates of the new quadrant as parameter 2.
WarpTravelCallback = Callable[[float, Coordinates], None]

WarpTravelCallbackV2 = Callable[[Coordinates], None]

TextureList = NewType('TextureList', List[Texture])
