
from typing import List
from typing import NewType
from typing import Union

from pytrek.gui.gamepieces.Commander import Commander
from pytrek.gui.gamepieces.Klingon import Klingon

Enemy   = NewType('Enemy',   Union[Klingon, Commander])
Enemies = NewType('Enemies', List[Enemy])


PhotonTorpedoId = NewType('PhotonTorpedoId', str)
EnemyTorpedoId  = NewType('EnemyTorpedoId', str)
EnemyFollowerId = NewType('EnemyFollowerId', str)
