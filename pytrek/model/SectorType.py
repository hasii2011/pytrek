from enum import Enum


class SectorType(Enum):

    UNKNOWN              = 'unknown'
    ENTERPRISE           = 'Enterprise'
    EMPTY                = 'empty'
    STAR                 = 'star'
    PLANET               = 'planet'
    STARBASE             = 'starbase'
    KLINGON              = 'klingon'
    COMMANDER            = 'commander'
    BLACK_HOLE           = 'blackhole'
    PHOTON_TORPEDO       = 'photonTorpedo'
    EXPLOSION            = 'explosion'
    KLINGON_TORPEDO      = 'klingonTorpedo'
    KLINGON_TORPEDO_MISS = 'klingonTorpedoMiss'
    ENTERPRISE_TORPEDO_MISS = 'enterpriseTorpedoMiss'
