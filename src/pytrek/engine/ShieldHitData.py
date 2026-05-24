
from typing import cast

from dataclasses import dataclass


@dataclass
class ShieldHitData:

    shieldAbsorptionValue:   float = cast(float, None)
    degradedTorpedoHitValue: float = cast(float, None)
