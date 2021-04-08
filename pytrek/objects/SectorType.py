from enum import Enum


class SectorType(Enum):

    UNKNOWN              = 'unknown'
    ENTERPRISE           = 'Enterprise'
    EMPTY                = 'empty'
    STAR                 = 'star'
    STARBASE             = 'starbase'
    KLINGON              = 'klingon'
    COMMANDER            = 'commander'
    BLACK_HOLE           = 'blackhole'
    PHOTON_TORPEDO       = 'photonTorpedo'
    EXPLOSION            = 'explosion'
    BIG_RED_X            = 'bigRedX'
    KLINGON_TORPEDO      = 'klingonTorpedo'
    KLINGON_TORPEDO_MISS = 'klingonTorpedoMiss'
