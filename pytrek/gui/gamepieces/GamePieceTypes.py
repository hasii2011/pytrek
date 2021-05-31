
from collections import namedtuple

from typing import List
from typing import NewType

Klingons  = NewType('Klingons', List[str])

KlingonId       = NewType('KlingonId', str)
PhotonTorpedoId = NewType('PhotonTorpedoId', str)

RadianInfo = namedtuple('RadianInfo', 'actualAngleRadians, angleDiffRadians')
