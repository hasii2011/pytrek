from enum import Enum


# noinspection SpellCheckingInspection
class SectorType(Enum):

    UNKNOWN              = 'Unknown'
    ENTERPRISE           = 'Enterprise'
    EMPTY                = 'Empty'
    STAR                 = 'Star'
    PLANET               = 'Planet'
    STARBASE             = 'Starbase'
    KLINGON              = 'Klingon'
    COMMANDER            = 'Commander'
    SUPER_COMMANDER      = 'SuperCommader'
    BLACK_HOLE           = 'Blackhole'
    PHOTON_TORPEDO       = 'PhotonTorpedo'
    EXPLOSION            = 'Explosion'
    KLINGON_TORPEDO      = 'KlingonTorpedo'
    KLINGON_TORPEDO_MISS = 'KlingonTorpedoMiss'
    ENTERPRISE_TORPEDO_MISS = 'EnterpriseTorpedoMiss'
