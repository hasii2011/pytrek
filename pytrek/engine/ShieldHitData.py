
from dataclasses import dataclass


@dataclass
class ShieldHitData:

    shieldAbsorptionValue:   float = None
    degradedTorpedoHitValue: float = None
