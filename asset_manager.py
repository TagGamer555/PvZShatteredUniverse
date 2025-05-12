import asset_path_generator
import sys
import os
import pygame
import state

# NB! Display is inited in main.py!

# Only load if this script is executed
if __name__ == "__main__":
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.display.init()
    pygame.display.set_mode((1, 1))

if len(sys.argv) > 1:
    root_folder = sys.argv[1]
else:
    root_folder = os.getcwd()

# get all png assets in a form of dictionary
# format: {"asset.png": "path/to/asset.png", ...}
pngs = asset_path_generator.find_pngs(root_folder)

cache = {"error": pygame.image.load(os.path.join(root_folder, "ASSETS", "error.png")).convert_alpha()}

def load_asset(asset):
    asset = asset.lower()
    # updated from list to dict for faster speed
    if asset in pngs:
        return pygame.image.load(pngs[asset]).convert_alpha()
    return cache["error"]

def load_asset_cache(asset, ext="png"):
    asset = asset.lower()
    ext = ext.lower()
    # god I love how you can just do "if asset in cache" and it sounds like english
    # python is da goat of readability
    if asset in cache: print("not loaded: exists")
    else:
        cache[asset] = load_asset(f"{asset}.{ext}") # pass on extension since it's required
        print("loaded: added to cache")

def forget_asset(asset):
    asset = asset.lower()
    if asset == "error": print("can't forget: error is mandatory")
    elif asset not in cache: print("can't forget: doesn't exist")
    else:
        cache.pop(asset)
        print("forgot: asset removed")

def load_image_autoscale_cache(asset, ext="png"):
    asset = asset.lower()
    ext = ext.lower()
    # god I love how you can just do "if asset in cache" and it sounds like english
    # python is da goat of readability
    if asset in cache: print("not loaded: exists")
    else:
        cache[asset] = load_asset(f"{asset}.{ext}") # pass on extension since it's required
        print("loaded: added to cache")

class GroupedAssetManager:
    def __init__(self):
        self.images = self.images or [] # create self.images if it doesn't exist yet to avoid `NameError` in self.load()
        self.load()
        self.autoscale()
    def load(self):
        for i in self.images:
            load_asset_cache(i)
    def unload(self):
        for i in self.images:
            forget_asset(i)

class LevelLoad(GroupedAssetManager):
    def __init__(self):
        self.images = []
        # load ALL plant images
        self.images += [i.__name__.lower() for i in state.all_seed_packets]
        # load ALL seed packet images
        self.images += [i+"_seedpacket" for i in self.images]
        # load ui and sundrops of size 25, 50, and 75
        self.images += [*[f"sundrop_{i*25}" for i in range(1, 4)], "uishovel", "uishovel_selected"]
        # load projectiles
        self.images += ["pea_proj", "star_proj"]
        # load zombies that are present in the level
        self.images += [i.__name__.lower() for i in state.zombie_types]
        # load misc images
        self.images += ["sunflower_glow"]
        super().__init__()

if __name__ == "__main__":
    LevelLoad()
