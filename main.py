# --------- imports ---------
import pygame as pg
from sys import exit
from random import uniform, randint, choice
import entities as e # I am lazy :( - NO MORE!
import state
import ui
import systems
import datetime



# --------- pre-load setup ---------
# pygame setup
pg.font.init()



# --------- settings ---------
# game settings
# (resolution, FPS, etc.)
#TODO: window resizing
WIDTH = 800
HEIGHT = 600
SCREEN = pg.display.set_mode((WIDTH, HEIGHT), pg.SRCALPHA)
CLOCK = pg.time.Clock()
FPS = 60
STARTING_SUN = 150 # og: 150 for reference



# --------- other data ---------
# load sprites and fonts here in the future
# 10/05/2025 - that future has come...
import asset_manager

# Import Drawable if it exists in entities or ui, or define a base Drawable class if needed
try:
    from entities import Drawable
except ImportError:
    try:
        from ui import Drawable
    except ImportError:
        class Drawable:
            def draw(self, surface):
                pass



# --------- helper functions ---------
# draw a checkerboard lawn
# this is a helper function for drawing the lawn (no shit)
def draw_lawn(color1, color2, startX, startY, rows, cols, tile_size, surface):
    for i in range(cols):
        for j in range(rows):
            x = startX + i * tile_size
            y = startY + j * tile_size
            
            # Checkerboard pattern
            if (i + j) % 2 == 0:
                color = color1
            else:
                color = color2
            
            pg.draw.rect(surface, color, (x, y, tile_size, tile_size))

def do_setup(starting_sun=STARTING_SUN, seed_packets=list(state.all_seed_packets)[:12], zombie_types=state.all_zombie_types, no_starting_cooldowns=False):
    state.sun = starting_sun
    state.seed_packets = seed_packets[:12] # limit to 12 to prevent future errors
    state.zombie_types = zombie_types

    if no_starting_cooldowns:
        state.seed_cooldowns = [0 for _ in state.seed_packets]
    else:
        state.seed_cooldowns = [i.starting_cooldown for i in state.seed_packets]



# --------- systems ---------
# see system.py
# used for autonomous systems in levels



# --------- entities ---------
# See entities.py. It stores creatures of this world, such as collectible sundrops, pea projectiles, peashooters, sunflowers, and even basic zombies.



# --------- setup ---------
# for future me:
# this section is perfect for starting new levels or loading them just give it some metadata from outside
# probably will have to create a game class at some point, not now though
rows = 5
cols = 9
tile_size = 70
lawn_x = (WIDTH - cols*tile_size) / 2
lawn_y = (HEIGHT - rows*tile_size) / 2

seed_packets = [e.Peashooter, e.Sunflower, e.WallNut]
do_setup(starting_sun=1500, no_starting_cooldowns=True, seed_packets=seed_packets)

# package metadata and send it to systems.py
systems.level_metadata = {
    "res_width": WIDTH,
    "res_height": HEIGHT,
    "lawn_rows": rows,
    "lawn_cols": cols,
    "tile_size": tile_size,
    "lawn_x": lawn_x,
    "lawn_y": lawn_y,
}

# shovel? - shovel!
ui.ShovelButton(WIDTH-90, HEIGHT-90, 70, 70)

# seed packets? - seed packets!
for i in range(len(state.seed_packets)):
    ui.SeedPacketSurvival(2.5, 100+45*i, 60, 40, state.seed_packets[i])

# sun counter
ui.SunCounter(35, 7.5)

# setup level (systems go brrr...)
systems.SYSTEM_NaturalSun(900, 50, (1,1))
systems.SYSTEM_ZombieWaves(1200, 60, 1.2, wave_limit=-1) # og: 1200 (20.0s) for reference

# the main course
tiles = [*["land"]*3,"water"]
tilemap = [[choice(tiles) for _ in range(9)] for _ in range(5)]
systems.SYSTEM_GenerateLawn(lawn_x, lawn_y, 70, 70, 5, 9, tilemap)



# --------- main game ---------
# main game loop

RUNNING = True
while RUNNING:
    for event in pg.event.get():
        # quit event (close window)
        if event.type == pg.QUIT: RUNNING = False
        
        # key events (keyboard input)
        if event.type == pg.KEYDOWN and event.key == pg.K_d:
            state.shovel_active = not state.shovel_active
            if state.selection: state.selection = None
        
        # F12 key event (screenshot)
        elif event.type == pg.KEYDOWN and event.key == pg.K_F12:
            pg.image.save(SCREEN, f"SCREENSHOTS\\screenshot-{str(datetime.date.today())+'-'+str(datetime.datetime.now().replace(microsecond=0).time()).replace(':','-')}.png")

        # 1-6, q-y key events (seed packets)
        for i in range(len(state.seed_packets)):
            # I am keeping this monster for showoff, don't you dare scold me for trying to make it my pet
            # edit: IT EVOLVED INTO A MULTI-LINER!!! EVERYONE, RUN! SCATTER! RUUUUN!!!!
            '''
            exec(f"""if event.type == pg.KEYDOWN and event.key == pg.K_{j+1} and len(state.seed_packets) >= {i+1} and state.sun >= state.seed_packets[{i}].sun_cost and seed_cooldowns[{i}] == 0 and state.selection != state.seed_packets[{i}]:
    state.selection = state.seed_packets[{i}]
elif event.type == pg.KEYDOWN and event.key == pg.K_{j+1} and state.selection == state.seed_packets[{i}]:
    state.selection = None""")
            '''
            # edit: I killed it, it's gone for good... Hopefully.
            # 22:05 (UTC+1) 04/05/2025: ui.py construction starts... NOW!
            # 11:29 (UTC+1) 05/05/2025: still doing it!
            # 12:34 (UTC+1) 05/05/2025: DONE!!!!!!! :D
            if event.type == pg.KEYDOWN:
                # list of keys to use
                keys = ["1", "2", "3", "4", "5", "6", "q", "w", "e", "r", "t", "y"]
                if eval(f"event.key == pg.K_{keys[i]}"): # no more j :(
                    
                    # Condition for selecting a seed
                    if len(state.seed_packets) >= i+1 and \
                       state.sun >= state.seed_packets[i].sun_cost and \
                       state.seed_cooldowns[i] == 0 and \
                       state.selection != state.seed_packets[i]:
                        state.selection = state.seed_packets[i]  # Select the seed
                        state.shovel_active = False
                        
                    # Condition for deselecting the seed
                    elif state.selection == state.seed_packets[i]:
                        state.selection = None  # Deselect the seed
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3: # mouse1 is 1, but mouse2 is 3???? WHYYYY
                # right mouse button
                # deselect everything using RMB!
                state.selection = None
                state.shovel_active = False
    
    for index in range(len(state.seed_cooldowns)):
        if state.seed_cooldowns[index] > 0:
            state.seed_cooldowns[index] -= 1

    # cls
    SCREEN.fill((35, 45, 55))

    for system in systems.SYSTEM_Root.instances.copy():
        system.update()
    
    for entity in e.Entity.instances.copy():
        entity.update(SCREEN)
    
    for element in ui.UI.instances.copy():
        element.update(SCREEN)

    # Gather all drawables
    drawables = []
    drawables.extend(e.Entity.instances.copy())
    drawables.extend(ui.UI.instances.copy())
    # If you have systems or other drawables, add them here

    # Sort by z value
    drawables.sort(key=lambda obj: obj.z if hasattr(obj, 'z') else 0)

    # Draw all to the main screen
    for obj in drawables:
        if isinstance(obj, Drawable):
            # If the draw method returns a surface and position, use BLEND_ADD
            result = obj.draw(SCREEN)
            if isinstance(result, tuple) and len(result) == 2:
                surf, pos = result
                # Use a configurable blending mode
                blending_mode = pg.BLEND_ADD  # Default blending mode
                SCREEN.blit(surf, pos, special_flags=blending_mode)
            elif result is not None:
                print(f"Warning: Unexpected return value from draw method of {obj}: {result}")

    # Update the screen
    pg.display.flip()
    
    CLOCK.tick(FPS) # I will probably not need delta time. Probably. I'll see
pg.quit()
exit()
