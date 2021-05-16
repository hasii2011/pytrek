
from enum import Enum


class DeviceType(Enum):

    ShortRangeSensors = 'Short-Range Sensors'
    LongRangeSensors  = 'Long-Range Sensors'
    Phasers           = 'Phasers'
    PhotonTubes       = 'Photon Tubes'
    LifeSupport       = 'Life Support'
    WarpEngines       = 'Warp Engines'
    ImpulseEngines    = 'Impulse Engines'
    Shields           = 'Shields'
    SubspaceRadio     = 'Subspace Radio'
    ShuttleCraft      = 'Shuttle Craft'
    Computer          = 'Computer'
    NavigationSystem  = 'Navigation System'
    Transporter       = 'Transporter'
    ShieldControl     = 'Shield Control'
    DeathRay          = 'Death Ray'
    SpaceProbe        = 'Space Probe'
    CAD               = 'Collision Avoidance Device'

    def __str__(self):
        return self.value

