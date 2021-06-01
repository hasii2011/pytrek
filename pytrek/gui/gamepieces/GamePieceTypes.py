
from typing import List
from typing import NewType

from pytrek.gui.gamepieces.Commander import Commander
from pytrek.gui.gamepieces.Klingon import Klingon

Klingons   = NewType('Klingons', List[Klingon])
Commanders = NewType('Commanders', List[Commander])

PhotonTorpedoId = NewType('PhotonTorpedoId', str)
