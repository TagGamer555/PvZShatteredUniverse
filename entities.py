import pygame as pg
from random import uniform
import state
import time #TODO: use later
import utils

# define Drawable
class Drawable:
    def draw(self, surface):
        pass

layers = ["platform", "main", "shell"]

# reworked the whole hp and damage numbers to be like in pvz2
# so reg plants now have 300 hp instead of 80 and zombies deal 100 DPS (1 attack/s)
# also wall-nut has 13.333... times the health of a reg plant, so 4000 (can withstand 40 hits before going down)
# and the zombies deal 100 DPS (1 attack/s) so they can kill a wall-nut in 40 seconds

class Entity(Drawable):
    instances = set()
    projectiles = set()
    
    def __init__(self, x, y, team, health):
        # coords
        self.x = x
        self.y = y
        # z-index
        self.z = state.BOTTOMGROUND
        # team
        self.team = team
        # health and max health
        self.health = health
        self.max_health = health
        # auxiliary variables
        self.random_range = (0.9, 1.1111111111)
        # add to the set of all entities
        # this is a set, so it won't have duplicates (ok Copilot)
        Entity.instances.add(self)
    
    def update(self, surface):
        self.die()
        self.behavior()
        self.draw(surface)
    
    # behavior of the entity
    def behavior(self): pass
    
    # draw the entity
    def draw(self, surface): pass
    
    # kill the entity
    def die(self):
        if self.health <= 0:
            Entity.instances.discard(self)
            #TODO: Remove from global grid, somehow.
            #Done, but there might be a faster way later on.
            #I think I found it after doing lawn tiles as buttons and not a list-dictionary mutant
            # are you sure? I think you just made it worse (THANKS COPILOT HAHA)
    
    def get_hitbox(self): return None

# sundrop collectible
#copilot: sundrop is a collectible that falls down and can be collected by the player
# hey copilot, do you wanna fall down and be collected by the player?
#copilot: no, I don't want to fall down and be collected by the player
class Sundrop(Entity):
    def __init__(self, x, y, health, value, x_vel, y_vel, y_accel, y_limit):
        super().__init__(x, y, "Resources", health)
        self.max_health = health
        self.value = value
        self.x_vel = x_vel
        self.y_vel = y_vel
        # no need for x acceleration since it just falls down
        self.y_accel = y_accel
        self.y_limit = y_limit
        self.existed_for = 0
        self.collected = False
    
    def behavior(self):
        self.existed_for += 1
        self.health -= 1
        mouse_x, mouse_y = pg.mouse.get_pos()
        if utils.dist(mouse_x, mouse_y, self.x, self.y) > self.value/2 and not self.collected:
            self.fall_down()
        else:
            self.collected = True
    
    def fall_down(self):
        if self.y < self.y_limit and self.y_limit - self.y > self.y_vel:
            self.y += self.y_vel
            self.y_vel += self.y_accel
            self.x += self.x_vel
        elif self.y < self.y_limit and self.y_limit - self.y <= self.y_vel:
            self.y = self.y_limit
            self.y_vel = 0
            self.y_accel = 0
    
    def draw(self, surface):
        if not self.collected:
            if self.health / self.max_health > 0.1:
                pg.draw.circle(surface, (255, 255, 0, min(255, self.existed_for*8)), (self.x, self.y), self.value/4)
            else:
                pg.draw.circle(surface, (255, 255, 0, max(0, min(255, self.health*8))), (self.x, self.y), self.value/4)
        else:
            pg.draw.circle(surface, (255, 255, 0, 255), (self.x, self.y), self.value/4)
    
    def die(self):
        if self.collected:
            sun_ui_coords = state.sun_ui_coords
            self.dist_to_sun_ui = utils.dist(*sun_ui_coords, self.x, self.y)
            if self.dist_to_sun_ui > 1: #TODO: Un-hardcode coords in the future - ima do it in the state.py - done
                self.x, self.y = utils.translate_point_degr(self.x, self.y, min(15, self.dist_to_sun_ui*0.1), utils.point2point_angle_degr(self.x, self.y, *sun_ui_coords))
            else:
                state.sun += self.value
                Entity.instances.discard(self)
        elif self.health <= 0:
            # you couldn't collect the sun??!???! how could you! >:(
            # remove the sundrop from the game after its lifetime is over
            Entity.instances.discard(self)



# --------- plants ---------

# backbone class for all Plants
class Plant(Entity):
    def __init__(self, x, y, health):
        super().__init__(x, y, "Plants", health)
        self.tile = None  # Set externally when planted
        self.z = state.MIDDLEGROUND
    
    # I'm lazy and most plants will have this hitbox anyway - ok but why are you lazy?
    def get_hitbox(self):
        size = 50
        return pg.Rect(self.x-size/2, self.y-size/2, size, size)
    
    def discard_externally(self):
        Entity.instances.discard(self)
    
    def __init_subclass__(cls, **kwargs):
        # add the plant to all plant seed packets so that the asset manager can load them
        super().__init_subclass__(**kwargs)
        state.all_seed_packets.add(cls)
    
    def die(self):
        if self.health <= 0:
            if self.tile:
                if self.tile.layers[self.layer] is self:
                    self.tile.layers[self.layer] = None
            Entity.instances.discard(self)

# pea
class Pea(Entity):
    def __init__(self, x, y, damage, angle):
        super().__init__(x, y, "Plants", 120)
        self.speed = 8 # Speed at which the pea moves
        self.damage = damage
        self.angle = angle
        self.z = state.FOREGROUND
        Entity.projectiles.add(self)
    
    def behavior(self):
        # updated peas to move in a direction rather than rightwards only by increm x by speed
        self.x, self.y = utils.translate_point_degr(self.x, self.y, self.speed, self.angle)
        self.health -= 1 # Lifetime
    
    def draw(self, surface):
        pg.draw.circle(surface, (127, 255, 0), (self.x, self.y), 10)  # Draw the pea as a circle
    
    def die(self):
        if self.health <= 0:
            Entity.instances.discard(self)
            Entity.projectiles.discard(self)
    
    def get_hitbox(self):
        radius = 10
        return pg.Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)

# star
class Star(Entity):
    def __init__(self, x, y, damage, angle):
        super().__init__(x, y, "Plants", 120)
        self.speed = 10
        self.damage = damage
        self.angle = angle
        self.z = state.FOREGROUND
        Entity.projectiles.add(self)
    
    def behavior(self):
        self.x, self.y = utils.translate_point_degr(self.x, self.y, self.speed, self.angle)
        self.health -= 1
    
    def draw(self, surface):
        pg.draw.circle(surface, (255, 255, 75), (self.x, self.y), 10)
    
    def die(self):
        if self.health <= 0:
            Entity.instances.discard(self)
            Entity.projectiles.discard(self)
    
    def get_hitbox(self):
        return pg.Rect(self.x - 10, self.y - 10, 20, 20)

# Peashooter
class Peashooter(Plant):
    sun_cost = 75
    cooldown = 450 # 7.5s
    starting_cooldown = 450 # 7.5s
    attack_range = 120
    localized_name = "Peashooter"
    layer = "main"
    terrain = ["land"]
    platform_type = []
    
    def __init__(self, x, y):
        super().__init__(x, y, 300)
        self.reload_reset = 90
        self.reload = self.reload_reset

    def behavior(self):
        if self.reload > 0:
            self.reload -= 1  # Decrease reload each frame
        elif self.target_found():
            # Shoot a pea when the reload is done and a target is found
            # maybe I'll add smth like puff-shrooms later on just for fun
            # since I already implemented the range in the Peashooter
            #SELF-REMINDER: Any common copy-pasta code goes into Entity class without question!
            self.shoot_pea()
            self.reload = int(self.reload_reset * uniform(*self.random_range))  # Reset the reload time

    def shoot_pea(self):
        # Create a new Pea entity at the Peashooter's position
        # updated with angle
        Pea(self.x, self.y, 20, 0)
    
    def draw(self, surface):
        pg.draw.rect(surface, (127, 255, 0), (self.x-25, self.y-25, 50, 50))  # Just a placeholder visual
    
    def target_found(self):
        for entity in Entity.instances.copy():
            if entity.team == "Zombies" and abs(entity.x - self.x) >= type(self).attack_range and entity.y == self.y:
                return True
        return False

# Sunflower
class Sunflower(Plant):
    sun_cost = 50
    cooldown = 600 # 10.0s
    starting_cooldown = 0 # 0s
    localized_name = "Sunflower"
    layer = "main"
    terrain = ["land"]
    platform_type = []
    
    def __init__(self, x, y):
        super().__init__(x, y, 300)
        self.reload_reset = 1200 # nerf from 20s to 25s - too fast, not sorry; nvm, I'm reveting - "reveting"?
        self.reload = int(self.reload_reset / 3) # gives back sun after placement faster
    
    def behavior(self):
        if self.reload > 0:
            self.reload -= 1
        else:
            self.produce_sun()
            self.reload = int(self.reload_reset * uniform(*self.random_range))
    
    def produce_sun(self):
        Sundrop(self.x, self.y, 600, 50, uniform(-5, 5), -8, 0.9, self.y + 30)
    
    def draw(self, surface):
        # light up before producing sun
        if self.reload / self.reload_reset < 0.1:
            pg.draw.rect(surface, (255, 255, 120), (self.x-25, self.y-25, 50, 50))
        else:
            pg.draw.rect(surface, (255, 190, 0), (self.x-25, self.y-25, 50, 50))

# Wall-Nut
class WallNut(Plant):
    sun_cost = 50
    cooldown = 1200 # 20.0s
    starting_cooldown = 1200 # 20.0s
    localized_name = "Wall-Nut"
    layer = "main"
    terrain = ["land"]
    platform_type = []
    
    def __init__(self, x, y):
        super().__init__(x, y, 3000) # ten times the health of a reg plant; nerfed to 5 times. yeah. buffed to 10 times again lol
        self.max_health = self.health # more setup trickery which *just works* :)
    
    def draw(self, surface):
        self.health_left_percent = self.health / self.max_health
        # >2/3 health left. We're okay
        if self.health_left_percent > 0.6666667:
            pg.draw.rect(surface, (142, 82, 82), (self.x-25, self.y-25, 50, 50))
        # >1/3 health left. A good amount hurt
        elif self.health_left_percent > 0.3333333:
            pg.draw.rect(surface, (91, 49, 56), (self.x-25, self.y-25, 50, 50))
        # >0 health left. "Oh crap we're dying"
        else:
            pg.draw.rect(surface, (66, 36, 51), (self.x-25, self.y-25, 50, 50))

# it's been so long since I added a new plant. brace yoselfs, for I am summoning the one and only... PUMPKIN!
# Pumpkin
class Pumpkin(Plant):
    sun_cost = 125 # +75 cost vs wall-nut
    cooldown = 1200 # 20.0s
    starting_cooldown = 1200 # 20.0s
    localized_name = "Pumpkin"
    layer = "shell"
    terrain = ["land"]
    platform_type = []
    
    def __init__(self, x, y):
        super().__init__(x, y, 3000) # same as wall-nut
        self.max_health = self.health
    
    def draw(self, surface):
        self.health_left_percent = self.health / self.max_health
        # >2/3 health left. We're okay
        if self.health_left_percent > 0.6666667:
            pg.draw.rect(surface, (249, 163, 27), (self.x-37.5, self.y, 75, 35))
        # >1/3 health left. A good amount hurt
        elif self.health_left_percent > 0.3333333:
            pg.draw.rect(surface, (250, 106, 10), (self.x-37.5, self.y, 75, 35))
        # >0 health left. "Oh crap we're dying"
        else:
            pg.draw.rect(surface, (223, 62, 35), (self.x-37.5, self.y, 75, 35))

# Cherry Bomb
class CherryBomb(Plant):
    sun_cost = 200
    cooldown = 2400 # 40.0s
    starting_cooldown = 2400 # 40.0s
    localized_name = "Cherry Bomb"
    layer = "main"
    terrain = ["land"]
    platform_type = []
    
    def __init__(self, x, y):
        super().__init__(x, y, 40) # here health is more of an animation progress rather than anything significant
        self.max_health = self.health
    
    # ban zombies from interacting with this at all
    def get_hitbox(self):
        pass
    
    def behavior(self):
        self.health -= 1
    
    def draw(self, surface):
        progress = self.max_health - self.health
        size = (70 - self.max_health) + min(self.max_health, progress)
        offset = size/2
        init_color = (223, 62, 35)
        red_progress = min(255 - init_color[0], int((255 - init_color[0]) / self.max_health * progress))
        green_progress = min(255 - init_color[1], int((255 - init_color[1]) / self.max_health * progress))
        blue_progress = min(255 - init_color[2], int((255 - init_color[2]) / self.max_health * progress))
        pg.draw.rect(surface, (init_color[0]+red_progress, init_color[1]+green_progress, init_color[2]+blue_progress), (self.x-offset, self.y-offset, size, size))
    
    def die(self):
        if self.health <= 0:
            for entity in Entity.instances:
                if self.x + 70 >= entity.x >= self.x - 70 and \
                   self.y - 70 <= entity.y <= self.y + 70 and \
                   entity.team == "Zombies":
                    entity.hurt(1800)
            if self.tile:
                if self.tile.layers[self.layer] is self:
                    self.tile.layers[self.layer] = None
            Entity.instances.discard(self)

# Terra-Fern
# a plant that can be placed on water tiles and acts as a platform like Lily Pad
# TODO: make it placeable on infertile land, and make it break ice blocks and graves when planted on them
# who wants to carry four tool plants that do one fucking job at a time
class TerraFern(Plant):
    sun_cost = 75
    cooldown = 600 # 10.0s
    starting_cooldown = 0 # 0.0s
    localized_name = "Terra-Fern"
    layer = "platform"
    terrain = ["water"]
    platform_type = ["land"]
    # FINISH TMRW
    # DOING IT!
    # done it (I think)
    #copilot: yes, you did it
    
    def __init__(self, x, y):
        super().__init__(x, y, 300)
        self.z = state.MIDDLEGROUND - 200
    
    def draw(self, surface):
        pg.draw.rect(surface, (26, 122, 62), (self.x-30, self.y-12.5, 60, 40))

# Starfruit
#copilot: a plant that shoots in five directions
class Starfruit(Plant):
    sun_cost = 175
    cooldown = 600 # 10.0s
    starting_cooldown = 600 # 10.0s
    attack_range = 150
    localized_name = "Starfruit"
    layer = "main"
    terrain = ["land"]
    platform_type = []
    
    def __init__(self, x, y):
        super().__init__(x, y, 300)
        self.reload_reset = 90
        self.reload = self.reload_reset

    def behavior(self):
        if self.reload > 0:
            self.reload -= 1
        elif self.target_found():
            self.shoot()
            self.reload = int(self.reload_reset * uniform(*self.random_range))

    def shoot(self):
        for i in [22.5, 337.5, 90, 270, 180]: Star(self.x, self.y, 30, i)
    
    def draw(self, surface):
        pg.draw.rect(surface, (255, 255, 75), (self.x-25, self.y-25, 50, 50))
    
    def target_found(self):
        target_angles = [22.5, 337.5, 90.0, 270.0, 180.0]
        epsilon = 2.0
        
        for entity in Entity.instances:
            if entity.team != "Zombies":
                continue
            
            angle = utils.point2point_angle_degr(self.x, self.y, entity.x, entity.y)
            angle = (angle + 360) % 360
            
            for ta in target_angles:
                if abs(angle - ta) < epsilon:
                    return True
        
        return False



# --------- zombies ---------

#copilot: the zombies are a bit different from the plants
# you mean... a *blit* different?
#copilot: yes, exactly

# backbone class for all Zombies
class Zombie(Entity):
    def __init__(self, x, y, health, armor_durability, armor_dr):
        super().__init__(x, y, "Zombies", health)
        self.attack_interval = type(self).attack_interval
        self.interval_progress = type(self).attack_interval
        self.armor_durability = armor_durability
        self.armor_dr = armor_dr
        self.z = state.MIDDLEGROUND + 200
    
    def attack_plant(self, damage):
        zombie_hitbox = self.get_hitbox()
        
        for entity in Entity.instances.copy():
            # fix: zombies will no longer try to attack the projectiles
            # edit: accidentally put this code in the hitreg script LOL
            for layer in reversed(layers):
                # update: attack shell plants first, then main, then platforms, etc.
                if entity.team == "Plants" and entity not in Entity.projectiles and hasattr(entity, 'get_hitbox') and type(entity).layer == layer:
                    plant_hitbox = entity.get_hitbox()
                    if plant_hitbox and zombie_hitbox.colliderect(plant_hitbox):
                        if self.interval_progress > 0:
                            self.interval_progress -= 1
                        else:
                            self.interval_progress = self.attack_interval
                            entity.health -= damage
                        return True # attacking a plant
        
        return False # not attacking anything
    
    def hitreg(self):
        zombie_hitbox = self.get_hitbox()
        for entity in Entity.projectiles.copy():
            if entity.team == "Plants" and hasattr(entity, 'get_hitbox'):
                if zombie_hitbox.colliderect(entity.get_hitbox()):
                    self.hurt(entity.damage)
                    entity.health = 0
    
    # helper method for calculating damage taken
    def hurt(self, amount):
        # save current armor durability for later
        precalc_durability = self.armor_durability
        # perfect damage reduction (DR)
        if self.armor_dr == 1 and self.armor_durability > 0:
            # apply damage to armor
            new_armor_durability = self.armor_durability - min(self.armor_durability, amount)
            # apply damage to health if armor couldn't block everything
            new_health = self.health - max(0, amount - self.armor_durability)
            # apply new values to properties
            self.armor_durability = new_armor_durability
            self.health = new_health
        # partial DR
        elif self.armor_durability > 0 and self.armor_dr > 0:
            # both health pool and armor durability should share the damage they take
            self.health -= amount - amount * self.armor_dr
            self.armor_durability -= amount * self.armor_dr
        # unarmored (no armor) or no DR
        elif self.armor_durability <= 0 or self.armor_dr == 0:
            # raw damage
            self.health -= amount
        
        # activates only once thru some "clever" logic
        # basically if before all calculations the armor existed (precalc_durability > 0)
        # and if after the calculations the armor was destroyed (self.armor_durability <= 0)
        # then we activate self.on_armor_break()
        # it works only once because if last calculation armor was 0 then when 'hurt' is called
        # then precalc_durability becomes 0 as well, which does not satisfy precalc_durability > 0
        # thereby stopping this from activating EVERY time the 'hurt' is called
        if precalc_durability > 0 and self.armor_durability <= 0: self.on_armor_break()
    
    #copilot: this method is called when the armor breaks
    #copilot: it can be overridden in subclasses to do something special
    # are you sure?
    #copilot: yes, I'm sure
    # are you sure?
    def on_armor_break(self):
        pass

# Basic Zombie
class BasicZombie(Zombie):
    localized_name = "Basic Zombie"
    spawn_cost = 1
    base_speed = 0.333333333 # 0.5 was a bit too fast for me; edit: 0.3333333 is too slow sadly; edit: 0.333333333 is bacc
    attack_interval = 60 # 20 was TOO fast. No, seriously. # 30 was too fast too. It's at 80 DPS rn.
    
    def __init__(self, x, y):
        super().__init__(x, y, 160, 0, 0)
        self.speed = type(self).base_speed # type(self) for flexibility and copy-paste-ability
    
    def get_hitbox(self):
        width, height = 30, 60
        return pg.Rect(self.x-15, self.y-30, width, height)
    
    def behavior(self):
        if not self.attack_plant(100):
            self.x -= self.speed
        
        self.hitreg()

    def draw(self, surface):
        pg.draw.rect(surface, (150, 100, 200), (self.x-15, self.y-30, 30, 60))

# you know what? I am tired of only having ONE zombie type. from now on, introducing coneheads! :D
# Conehead Zombie
class ConeheadZombie(Zombie):
    localized_name = "Conehead Zombie"
    spawn_cost = 3 # more than two browncoats because yes
    # since helmet zombies are just basic zombies with, well helmets
    # it'd be fair to copy the boring stats from the basic zombie
    base_speed = BasicZombie.base_speed
    attack_interval = BasicZombie.attack_interval
    
    def __init__(self, x, y):
        super().__init__(x, y, 160, 160, 1.0)
        self.speed = type(self).base_speed
    
    def get_hitbox(self):
        width, height = 30, 60
        return pg.Rect(self.x-15, self.y-30, width, height)
    
    def behavior(self):
        if not self.attack_plant(100):
            self.x -= self.speed
        
        self.hitreg()

    def draw(self, surface):
        pg.draw.rect(surface, (150, 100, 200), (self.x-15, self.y-30, 30, 60))
        if self.armor_durability > 0:
            # make him visually wear a "cone" because it's necessary (true fact) (trust me bro) (real)
            pg.draw.rect(surface, (255, 175, 75), (self.x-15, self.y-40, 30, 20))

# Buckethead Zombie
#copilot: this is a copy-paste of the Conehead Zombie, but with different stats
class BucketheadZombie(Zombie):
    localized_name = "Buckethead Zombie"
    spawn_cost = 5 # five normal zombies
    # since helmet zombies are just basic zombies with, well helmets
    # it'd be fair to copy the boring stats from the basic zombie
    base_speed = BasicZombie.base_speed
    attack_interval = BasicZombie.attack_interval
    
    def __init__(self, x, y):
        super().__init__(x, y, 160, 240, 1.0)
        self.speed = type(self).base_speed
    
    def get_hitbox(self):
        width, height = 30, 60
        return pg.Rect(self.x-15, self.y-30, width, height)
    
    def behavior(self):
        if not self.attack_plant(100):
            self.x -= self.speed
        
        self.hitreg()

    def draw(self, surface):
        pg.draw.rect(surface, (150, 100, 200), (self.x-15, self.y-30, 30, 60))
        if self.armor_durability > 0:
            pg.draw.rect(surface, (175, 175, 175), (self.x-15, self.y-40, 30, 20))

# Brickhead Zombie
# just a tougher buckethead
class BrickheadZombie(Zombie):
    localized_name = "Brickhead Zombie"
    spawn_cost = 7 # seven normal zombies
    # since helmet zombies are just basic zombies with, well helmets
    # it'd be fair to copy the boring stats from the basic zombie
    base_speed = BasicZombie.base_speed
    attack_interval = BasicZombie.attack_interval
    
    def __init__(self, x, y):
        super().__init__(x, y, 160, 360, 1.0)
        self.speed = type(self).base_speed
    
    def get_hitbox(self):
        width, height = 30, 60
        return pg.Rect(self.x-15, self.y-30, width, height)
    
    def behavior(self):
        if not self.attack_plant(100):
            self.x -= self.speed
        
        self.hitreg()

    def draw(self, surface):
        pg.draw.rect(surface, (150, 100, 200), (self.x-15, self.y-30, 30, 60))
        if self.armor_durability > 0:
            pg.draw.rect(surface, (175, 100, 75), (self.x-15, self.y-40, 30, 20))
