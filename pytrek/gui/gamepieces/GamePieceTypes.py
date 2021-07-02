
from typing import List
from typing import NewType

from pytrek.gui.gamepieces.base.BaseEnemy import BaseEnemy

Enemy   = NewType('Enemy',   BaseEnemy)
Enemies = NewType('Enemies', List[Enemy])


PhotonTorpedoId = NewType('PhotonTorpedoId', str)
EnemyTorpedoId  = NewType('EnemyTorpedoId', str)
EnemyFollowerId = NewType('EnemyFollowerId', str)
