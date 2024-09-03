
from enum import Enum


# noinspection SpellCheckingInspection
class FutureEventType(Enum):

    SPY                             = 'Spy'                     # spy event happens always (no future[] entry)    FSPY
    SUPER_NOVA                      = 'Super Nova'              # Supernova                                       FSNOVA
    TRACTOR_BEAM                    = 'Tractor Beam'            # Commander tractor beams Enterprise              FTBEAM
    TIME_WARP_SNAPSHOT              = 'Time Warp Snapshot'      # Snapshot for time warp                          FSNAP
    COMMANDER_ATTACKS_BASE          = 'Cmdr Attacks Base'       # Commander attacks base                          FBATTAK
    COMMANDER_DESTROYS_BASE         = 'Cmdr Destroys Base'      # Commander destroys base                         FCDBAS
    SUPER_COMMANDER_MOVES           = 'SCmdr Moves'             # Super Commander moves (might attack base)       FSCMOVE
    SUPER_COMMANDER_DESTROYS_BASE   = 'SCmdr Destroys Base'     # Super Commander destroys base                   FSCDBAS
    MOVE_DEEP_SPACE_PROBE           = 'Move Deep Space Probe'   # Move deep space probe                           FDSPROB
    NOT_SET                         = 'Not Set'                 # Used to indicate a no value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
