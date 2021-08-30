
from enum import Enum


class FutureEventType(Enum):

    SPY                             = 0   # spy event happens always (no future[] entry)    FSPY
    SUPER_NOVA                      = 1   # Supernova                                       FSNOVA
    TRACTOR_BEAM                    = 2   # Commander tractor beams Enterprise              FTBEAM
    TIME_WARP_SNAPSHOT              = 3   # Snapshot for time warp                          FSNAP
    COMMANDER_ATTACKS_BASE          = 4   # Commander attacks base                          FBATTAK
    COMMANDER_DESTROYS_BASE         = 5   # Commander destroys base                         FCDBAS
    SUPER_COMMANDER_MOVES           = 6   # Super Commander moves (might attack base)       FSCMOVE
    SUPER_COMMANDER_DESTROYS_BASE   = 7   # Super Commander destroys base                   FSCDBAS
    MOVE_DEEP_SPACE_PROBE           = 8   # Move deep space probe                           FDSPROB

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
