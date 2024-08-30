
CONSOLE_SECTION_HEIGHT:       int = 190

COMMAND_INPUT_HEIGHT:   int = 20
COMMAND_SECTION_HEIGHT: int = COMMAND_INPUT_HEIGHT * 2
COMMAND_SECTION_WIDTH:  int = 200


SCREEN_WIDTH:     int = 800
SCREEN_HEIGHT:    int = 640 + CONSOLE_SECTION_HEIGHT + COMMAND_SECTION_HEIGHT

QUADRANT_GRID_WIDTH:  int = 640
QUADRANT_GRID_HEIGHT: int = 640

STATUS_VIEW_WIDTH: int = SCREEN_WIDTH - QUADRANT_GRID_WIDTH

QUADRANT_PIXEL_HEIGHT: int = 64
QUADRANT_PIXEL_WIDTH:  int = 64

QUADRANT_Y_ADJUSTMENT: int = CONSOLE_SECTION_HEIGHT + COMMAND_SECTION_HEIGHT

QUADRANT_ROWS:    int = 10
QUADRANT_COLUMNS: int = 10

GALAXY_ROWS:    int = 10
GALAXY_COLUMNS: int = 10

MINIMUM_COORDINATE: int = 0     # These should match the galaxy/quadrant size
MAXIMUM_COORDINATE: int = 9     # Currently, assumed that are the same size

STANDARD_SPRITE_WIDTH:  int = 32
STANDARD_SPRITE_HEIGHT: int = 32

HALF_QUADRANT_PIXEL_WIDTH:  int = QUADRANT_PIXEL_WIDTH // 2
HALF_QUADRANT_PIXEL_HEIGHT: int = QUADRANT_PIXEL_HEIGHT // 2

APPLICATION_NAME:        str = 'pytrek'
THE_GREAT_MAC_PLATFORM:  str = 'darwin'
GAME_SETTINGS_FILE_NAME: str = f'{APPLICATION_NAME}.ini'
BACKUP_SUFFIX:           str = '.bak'

MIN_SECTOR_X_COORDINATE: int = 0
MAX_SECTOR_X_COORDINATE: int = QUADRANT_COLUMNS - 1
MIN_SECTOR_Y_COORDINATE: int = 0
MAX_SECTOR_Y_COORDINATE: int = QUADRANT_ROWS - 1

MIN_QUADRANT_X_COORDINATE: int = 0
MAX_QUADRANT_X_COORDINATE: int = GALAXY_COLUMNS - 1
MIN_QUADRANT_Y_COORDINATE: int = 0
MAX_QUADRANT_Y_COORDINATE: int = GALAXY_ROWS - 1

FIXED_WIDTH_FONT_NAME:     str = 'UniverseCondensed'
FIXED_WIDTH_FONT_FILENAME: str = f'{FIXED_WIDTH_FONT_NAME}.ttf'

MINIMUM_WARP_FACTOR_VALUE: float = 1.0   # Below 1.0 is considered impulse speed
MAXIMUM_WARP_FACTOR_VALUE: float = 10.0  # The theoretical max warp speed

MINIMUM_SAFE_WARP_FACTOR:  float = 6.0   # Travel faster than this and you may damage warp engines

MILLISECONDS: float = 1000.0       # milliseconds in a second, duh !!
