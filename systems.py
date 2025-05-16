import entities
import ui
from random import uniform, randint, choice
import state
# 05/05/2025: first ever pygame-free script, no way

level_metadata = {} # receives metadata automatically from main.py on level boot
# it should get the following:
# res_width
# res_height
# lawn_rows
# lawn_cols
# tile_size
# lawn_x
# lawn_y

# this is the root class for all systems
# it is used to create a singleton system that can be updated
class SYSTEM_Root:
    instances = set()
    
    def __init__(self):
        SYSTEM_Root.instances.add(self)
    
    def update(self):
        pass

# this class is used to spawn sun drops
# it spawns them at a random position on the screen
class SYSTEM_NaturalSun(SYSTEM_Root):
    def __init__(self, interval, amount, random_range):
        super().__init__()
        self.interval = interval
        self.delay = self.interval
        self.amount = amount
        self.random_range = random_range
    
    def update(self):
        super().update()
        if self.delay > 0:
            self.delay -= 1
        else:
            entities.Sundrop(uniform(level_metadata["res_width"]/2+40, level_metadata["res_width"]/2-40), -10, 600, self.amount, 0, 3, 0, 180 + 70 * randint(0,4))
            self.delay = int(self.interval * uniform(*self.random_range))

# this class is used to spawn zombies in waves
# it spawns them in waves, with a delay between each zombie
class SYSTEM_ZombieWaves(SYSTEM_Root):
    def __init__(self, base_interval, spawn_delay, difficulty_multiplier, wave_limit=-1):
        super().__init__()
        self.state = "COOLDOWN"  # COOLDOWN or IN_PROGRESS
        self.zombie_types = state.zombie_types
        self.zombie_costs = [z.spawn_cost for z in self.zombie_types]
        self.difficulty_multiplier = difficulty_multiplier
        
        self.base_interval = base_interval
        self.spawn_delay = spawn_delay  # time between zombies in a wave
        self.wave_timer = base_interval
        self.spawn_timer = 0
        
        self.wave_limit = wave_limit
        self.current_wave = 0
        self.zombies_to_spawn = []
        self.credit = 0
    
    def update(self):
        super().update()
        
        if self.state == "COOLDOWN":
            self.wave_timer -= 1
            if self.wave_timer <= 0:
                self.start_new_wave()
        elif self.state == "IN_PROGRESS":
            self.handle_spawning()
        
        if self.wave_limit != -1 and self.current_wave >= self.wave_limit and not self.zombies_to_spawn:
            SYSTEM_Root.instances.discard(self) # level is over
    
    def start_new_wave(self):
        self.current_wave += 1
        self.credit = int((self.current_wave ** 1.3) * self.difficulty_multiplier)
        self.zombies_to_spawn = self.generate_wave(self.credit)
        self.state = "IN_PROGRESS"
        self.spawn_timer = self.spawn_delay
    
    def handle_spawning(self):
        if self.zombies_to_spawn:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                selected = self.zombies_to_spawn.pop(0)
                selected(level_metadata["res_width"] + 20, 160 + 70 * randint(0, 4))
                self.spawn_timer = self.spawn_delay
        else:
            self.state = "COOLDOWN"
            self.wave_timer = max(300, int(self.base_interval * (0.95 ** self.current_wave)))  # shorten interval slightly each wave
    
    def generate_wave(self, credit):
        wave = []
        attempts = 0
        while credit >= min(self.zombie_costs) and attempts < 100:
            z_class = choice(self.zombie_types)
            if z_class.spawn_cost <= credit:
                wave.append(z_class)
                credit -= z_class.spawn_cost
            attempts += 1
        return wave

# this class is used to generate the lawn
# it takes a tilemap and generates the lawn based on the tilemap
# the tilemap is a 2D array of strings, where each string represents a type of tile
class SYSTEM_GenerateLawn(SYSTEM_Root):
    def __init__(self, lawn_x, lawn_y, tile_width, tile_height, lawn_rows, lawn_cols, tilemap):
        self.lawn_x = lawn_x
        self.lawn_y = lawn_y
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.lawn_rows = lawn_rows
        self.lawn_cols = lawn_cols
        self.tilemap = tilemap
        self.generate()
    
    def check_tilemap_validity(self):
        if len(self.tilemap) == self.lawn_rows:
            lane_bools = set() # let's not waste ram with duplicates (even if it's minor); if at least one element is False, all() will fail anyway
            for i in self.tilemap:
                lane_bools.add(len(i) == self.lawn_cols)
            if all(lane_bools):
                return True
        return [["land" for _ in range(self.lawn_cols)] for _ in range(self.lawn_rows)]
    
    def create_lawn(self):
        # Iterate through the tilemap's rows and columns to create LawnTile instances
        for row_index, row in enumerate(self.tilemap):
            for col_index, terrain_type in enumerate(row):
                # Calculate the x and y position of the tile
                x_pos = self.lawn_x + (col_index * self.tile_width)
                y_pos = self.lawn_y + (row_index * self.tile_height)
                
                # Determine if the tile should have an alternating color pattern (checkerboard)
                alt = (row_index + col_index) % 2 == 1  # Alternates when the sum of indices is odd
                
                # Create the LawnTile instance
                ui.LawnTile(x_pos, y_pos, self.tile_width, self.tile_height, terrain_type, alt)
    
    def generate(self):
        if self.check_tilemap_validity(): self.create_lawn()
