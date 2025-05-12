# --------- log ---------
# dd/mm/yyyy: lorem ipsum
# lorem ipsum
# - lorem ipsum
# * lorem ipsum

# 03/05/2025: I started my project, did plants, planting, and basic rendering. The foundation was being laid.

# 04/05/2025: Here I am, coding zombies, shovel, and other shenanigans.
# I wonder for how long I'll be able to uphold this project without getting bored.
# Hopefully I'll finally make a functioning game... I'll see
# PLAN OF ACTION:
# * Make ui.py module
# * Move shovel to the bottom right like in pvz2
# * Turn grid list into a 3D tensor
# * Multiple terrain types; for now, just water and land
# * Multiple types of plants per tile, e.g. Lily Pad + Pumpkin + Peashooter
# * Pausing and speed-up working + ui buttons
# * "Ready, Set, Plant!" countdown before level begins
# * Flags (major waves)

# 05/05/2025: hi
# REVISED PLANT OF ACTION:
# - ui.py made, add more button classes so I can add them here - added shovel! - FULLY DONE!
# - shovel to be repositioned - DONE!
# - grid to be tensor-ified - DONE!
# - terrain to be added
# - multi-plant to be added - DONE!
# - NO MORE SPEEDING UP OR PAUSING UNTIL I CAN FIGURE IT OUT MYSELF
# - - I am considering using the 'time' module, but it'll time a significant amount of time (ha!) to restructure my tickers to time-based stuff
# - countdown to be implemented - this one will require pausing or some sort of "layered loading" to the level... but that would be less than ideal.
# - - I'll probably implement the countdown when I'll have my hands on pausing and speeding up, so that I can pause everything else while the countdown does its thing
# - flags to be done - I could do this right after terrain I think

# 08/05/2025:
# my keyboard's not living the best life right now
# I got the perfect damage reduction (DR) case handling for zombies with helmets cuz they resist cherry bombs and me no like dat

# 09/05/2025:
# replacin' tensors with something more epic, I'll tell ye later what it is ;)
# finish the ui.py, it's nearly done

# 10/05/2025:
# hi I'm back :)
# - entities.py could use ECS system (do later, this is a long-term goal rather than immediate emergency)
# - finish LawnTile class in ui.py
# - do lawn creation system in systems.py
# - maybe it's time to `time`? tickers are not very precise (1 tick is 16.67 ms) and very FPS-dependant so uhh yeah
# finally, it's about 17:33 and I've finally transitioned from tensors to buttons regarding lawn
# and also some other neat features along the way, like MULTIPLE TERRAIN SUPPORT!!!!!111!!!!1111 LETS GO BABYYYYYYYY
# z-layers would also be nice, since python uses a very fast Timsort for repetitive or near-completed data, which is basically what I'm going to have for z ordering
# asset manager finished: it loads, caches, and forgets
# started working on the Terra-Fern
# NOT happy with the current plant sprites, will very likely (DEFINITELY, actually) re-do, but later (after I am certain that everything works)
# auto-resizer-on-load not done yet
# sprites aren't actually loaded or used right now, but the logic is done
# tmrw I'll finish the Terra-Fern plant and FINALLY make the game not look like squares and circles
# ALSO! I need to make seed_packet_image_generator because:
# 1) I am too lazy to manually do EVERY image for EVERY seed packet. what if I want to change the background? I'll have to redraw the entire image!
# 2) I can use custom font that dynamically updates with my shit balancing!
# 3) come on, automation is super fun... (I am a Factorio, Satisfactory, and Mindustry addict #1; have tried Shapez but never bought, whoopsies!)

# 11/05/2025:
# doing the Terra-Fern right now
# JUST CAME UP WITH AN IDEA:
# Rotobaga and Starfruit, instead of using raycasts to check if a zombie threat exists in range
# could simply check if a slope between two points is correct for the projectile trajectory
# since they fire in straight lines
# I could also technically use this for the Peashooter, but a simple x-coord equality check never hurts, right?
# also, if (x2 - x1) in m = (y2 - y1) / (x2 - x1) is equal to 0, we're dividing by zero
# so use a try/except and return float('inf') instead (ezpz)
# HELL YEAH, MATH!!!!
# --- updates
# Terra-Fern as a Lily Pad is done; in the future, I'll add Flower Pot, Hot Potato, and Grave Buster behavior to it (so you don't carry 1236123 tool plants)
# also zlayers will have to wait, the system I'm currently using needs refactoring in best case scenario and complete rewriting in worst
# 12:43 - did Starfruit, and used angles instead of slopes using atan2. turns out I already had coords between two points to angle converter sooooooo
# 12:45 - imma start doing sprites and autoscaling



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
pg.font.init()



# --------- settings ---------
WIDTH = 800
HEIGHT = 600
SURFACES = {"SCREEN":pg.display.set_mode((WIDTH, HEIGHT), pg.SRCALPHA),
            "BG":pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA),
            "MG":pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA),
            "MG+":pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA),
            "MG++":pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA),
            "FG":pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA),
            "UI":pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA),
            "UI+":pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA),
            "UI++":pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)}
CLOCK = pg.time.Clock()
FPS = 60
STARTING_SUN = 1500 # og: 150 for reference



# --------- other data ---------
# load sprites and fonts here in the future
# 10/05/2025 - that future has come...
import asset_manager



# --------- helper functions ---------
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



# --------- systems ---------
# see system.py
# used for autonomous systems in levels



# --------- entities ---------
# See entities.py. It stores creatures of this world, such as collectible sundrops, pea projectiles, peashooters, sunflowers, and even basic zombies.



# --------- setup ---------
# for future me:
# this section is perfect for starting new levels or loading them just give it some metadata from outside
# probably will have to create a game class at some point, not now though
state.sun = STARTING_SUN

rows = 5
cols = 9
tile_size = 70
lawn_x = (WIDTH - cols*tile_size) / 2
lawn_y = (HEIGHT - rows*tile_size) / 2

state.seed_packets = [e.Peashooter, e.Sunflower, e.WallNut, e.Pumpkin, e.CherryBomb, e.TerraFern, e.Starfruit]
state.seed_packets = state.seed_packets[0:12] # only use the first 12 plants
state.seed_cooldowns = [i.starting_cooldown for i in state.seed_packets]

# sike ( temporary )
state.seed_cooldowns = [0 for _ in state.seed_packets]

state.zombie_types = [e.BasicZombie, e.ConeheadZombie, e.BucketheadZombie]
state.selection = None

# for memories
'''
# grid setup
layers = e.layers # here be different plant layers from the entities.py, such as "main" and "shell"
# entities also have a "layer" property
grid = [[{layers[i]: None for i in range(len(layers))} for _ in range(cols)] for _ in range(rows)]
'''

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
systems.SYSTEM_ZombieWaves(120, 60, 1.2, wave_limit=-1) # og: 1200 (20.0s) for reference

# the main course
tiles = [*["land"]*3,"water"]
tilemap = [[choice(tiles) for _ in range(9)] for _ in range(5)]
systems.SYSTEM_GenerateLawn(lawn_x, lawn_y, 70, 70, 5, 9, tilemap)



# --------- main game ---------
RUNNING = True
while RUNNING:
    for event in pg.event.get():
        if event.type == pg.QUIT: RUNNING = False
        
        if event.type == pg.KEYDOWN and event.key == pg.K_d:
            state.shovel_active = not state.shovel_active
            if state.selection: state.selection = None
        
        elif event.type == pg.KEYDOWN and event.key == pg.K_F12:
            pg.image.save(SURFACES["SCREEN"], f"SCREENSHOTS\\screenshot-{str(datetime.date.today())+'-'+str(datetime.datetime.now().replace(microsecond=0).time()).replace(':','-')}.png")
        
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
                # deselect everything using RMB!
                state.selection = None
                state.shovel_active = False
    
    for index in range(len(state.seed_cooldowns)):
        if state.seed_cooldowns[index] > 0:
            state.seed_cooldowns[index] -= 1
    
    for surface in SURFACES:
        SURFACES[surface].fill((0, 0, 0, 0)) # OH MY GOD YOU ARE MY SAVIOR!!! I AM CRYING FOR I HAVE FOUND YOU!!!!! THANK GOD!!!!! ;D
    SURFACES["SCREEN"].fill((35, 45, 55))
    
    for system in systems.SYSTEM_Root.instances.copy():
        system.update()
    
    for entity in e.Entity.instances.copy():
        entity.update(SURFACES)
    
    for thing in ui.UI.instances.copy():
        thing.update(SURFACES)
    
    # blit layer by layer (I hope the coordinates are right)
    SURFACES["SCREEN"].blit(SURFACES["BG"], (0, 0))
    SURFACES["SCREEN"].blit(SURFACES["MG"], (0, 0))
    SURFACES["SCREEN"].blit(SURFACES["MG+"], (0, 0))
    SURFACES["SCREEN"].blit(SURFACES["MG++"], (0, 0))
    SURFACES["SCREEN"].blit(SURFACES["FG"], (0, 0))
    SURFACES["SCREEN"].blit(SURFACES["UI"], (0, 0))
    SURFACES["SCREEN"].blit(SURFACES["UI+"], (0, 0))
    SURFACES["SCREEN"].blit(SURFACES["UI++"], (0, 0))
    
    pg.display.flip()
    
    CLOCK.tick(FPS) # I will probably not need delta time. Probably. I'll see
pg.quit()
exit()
