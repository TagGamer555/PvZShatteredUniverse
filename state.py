# THE NO IMPORTS LAND!

# --------- game state ---------
# Game state variables
# (global variables)
# - coding software: global offensive (CS:GO)

# amount of sun the player has (int)
sun = 0

# currently selected seed packet (class)
selection = None

# whether the shovel is active (bool)
shovel_active = False

# list of seed packets (list of classes)
# (e.g. Peashooter, Sunflower, etc.)
seed_packets = []

# list of seed packet cooldowns (list of ints)
seed_cooldowns = []

# list of zombie types (list of classes)
zombie_types = []

# all available plants (list of classes)
all_seed_packets = set()

# all available zombies (list of classes)
all_zombie_types = set()

# coordinates of the sun counter (tuple of ints)
sun_ui_coords = (20, 20)

# sprites required (list of strs)
require_sprites = []

# layer constants
# these are used to determine the order in which entities are drawn
# the lower the value, the further back it is drawn
BOTTOMGROUND = 0 # behind everything
BACKGROUND = 10000 # background
MIDDLEGROUND = 20000 # middle ground
FOREGROUND = 30000 # foreground
UIGROUND = 40000 # ui-level
