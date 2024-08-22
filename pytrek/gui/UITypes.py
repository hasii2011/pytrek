
from typing import Callable
from typing import List
from typing import NewType

from arcade import Texture

from pytrek.model.Coordinates import Coordinates

WarpTravelCallbackV2 = Callable[[Coordinates], None]

TextureList = NewType('TextureList', List[Texture])
