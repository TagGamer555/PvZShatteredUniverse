import pygame as pg
import state
import entities

pg.font.init()
Arial_24_bold = pg.font.SysFont("Arial", 24, bold=True)

# define Drawable
class Drawable:
    def draw(self, surface):
        pass

# TODO: TOMORROW PLEASE!!! I BEG YOU CONTINUE THIS PROJECT!!! PLEASE!!!
# tmrw: I'm here you idiot

# changed 'surface' to 'surface' for consistency
# lmao oops

# --------- core ---------

# base class for all UI-related stuff
class UI(Drawable):
    instances = set()
    
    # startup variable assignment and preparation
    def __init__(self, x, y, hitbox_w, hitbox_h):
        UI.instances.add(self)
        self.x = x
        self.y = y
        self.z = state.UIGROUND
        self.hitbox_w = hitbox_w
        self.hitbox_h = hitbox_h
        self.activated = False
    
    # main classmethod for updating everything
    def update(self, surface):
        self.behavior()
        self.draw(surface)
    
    # your display logic goes here
    def draw(self, surface):
        pass
    
    # your active logic (e.g. on mouse clicks) goes here
    def behavior(self):
        pass
    
    # discard this UI instance
    def discard(self):
        UI.instances.discard(self)
    
    # helper method for determining cursor collision
    def is_colliding_with_pointer(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        # I made three whole mistakes in this condition alone. Wow.
        return (self.x <= mouse_x <= self.x + self.hitbox_w and
                self.y <= mouse_y <= self.y + self.hitbox_h)

# base class for buttons and such
class Button(UI):
    def __init__(self, x, y, hitbox_w, hitbox_h, button_type, mouse_button=0):
        super().__init__(x, y, hitbox_w, hitbox_h)
        self.button_type = button_type
        self.mouse_button = mouse_button
        self.button_clicked = False
        # supported button types:
        # - CLICK
        # - HOLD
        # NB! If you are using an unsupported type, the button will be non-interactable!
    
    def behavior(self):
        super().behavior()
        if self.button_type == "CLICK" and self.is_clicked(): self.on_activation()
        elif self.button_type == "HOLD" and self.is_held(): self.on_activation()
    
    def is_clicked(self):
        mouse_pressed = pg.mouse.get_pressed()[self.mouse_button]
        if self.is_colliding_with_pointer():
            if mouse_pressed and not self.activated:
                self.activated = True
                return True
            elif not mouse_pressed:
                self.activated = False
        else:
            if not mouse_pressed:
                self.activated = False
        return False
    
    def is_held(self):
        mouse_pressed = pg.mouse.get_pressed()[self.mouse_button]
        if self.is_colliding_with_pointer():
            if mouse_pressed:
                self.activated = True
            else:
                self.activated = False
        elif not mouse_pressed:
            self.activated = False
        return self.activated
    
    def on_activation(self):
        pass



# --------- game ui ---------

# Shovel
class ShovelButton(Button):
    def __init__(self, x, y, hitbox_w, hitbox_h):
        super().__init__(x, y, hitbox_w, hitbox_h, "CLICK")
        self.icon_rect = pg.Rect(self.x, self.y, self.hitbox_w, self.hitbox_h)
    
    def on_activation(self):
        state.shovel_active = not state.shovel_active
        if state.selection: state.selection = None
    
    def draw(self, surface):
        shovel_color = (140, 100, 60) if not state.shovel_active else (255, 220, 100)
        
        pg.draw.rect(surface, shovel_color, self.icon_rect)
        
        shovel_label = Arial_24_bold.render("Shovel", True, (240, 240, 240))
        
        surface.blit(shovel_label, (self.icon_rect.x + 5, self.icon_rect.y + 25))
        
        if state.shovel_active: pg.draw.rect(surface, (255, 255, 0), self.icon_rect, 3)

# Seed Packet
class SeedPacketSurvival(Button):
    def __init__(self, x, y, hitbox_w, hitbox_h, plant):
        super().__init__(x, y, hitbox_w, hitbox_h, "CLICK")
        self.plant = plant
        self.get_cooldown() # test check
    
    def get_cooldown(self):
        try:
            # try to find the cooldown of the plant this seed packet has been assigned to
            return state.seed_cooldowns[state.seed_packets.index(self.plant)]
        except ValueError:
            # not found? discard it.
            self.discard()
    
    def on_activation(self):
        cooldown_satisfied = (self.get_cooldown() <= 0)
        price_satisfied = (state.sun >= self.plant.sun_cost)
        if cooldown_satisfied and price_satisfied:
            if not state.selection:
                state.selection = self.plant
                if state.shovel_active: state.shovel_active = not state.shovel_active
            else:
                state.selection = None
    
    def draw(self, surface):
        # "ah crap here we go again" (still doing code modularization!!)
        # edit: done soon-ish *exhales*
        
        # Background box
        pg.draw.rect(surface, (60, 60, 60), (self.x, self.y, self.hitbox_w, self.hitbox_h), border_radius=0)

        # Cooldown overlay
        if self.get_cooldown() > 0:
            cd_ratio = self.get_cooldown() / self.plant.cooldown
            cd_height = int(self.hitbox_h * cd_ratio)
            pg.draw.rect(surface, (0, 0, 0, 180), (self.x, self.y, self.hitbox_w, cd_height), border_radius=0)

        # Affordability indicator
        if state.sun < self.plant.sun_cost:
            label = Arial_24_bold.render(str(self.plant.sun_cost), True, (255, 0, 0))
        else:
            label = Arial_24_bold.render(str(self.plant.sun_cost), True, (255, 255, 255))

        # Draw label or image (placeholder with cost)
        cost_length = len(str(self.plant.sun_cost))
        surface.blit(label, (self.x + self.hitbox_w - self.hitbox_w/(5/cost_length), self.y + self.hitbox_h - self.hitbox_h/1.5))

        # state.selection border (OOPS this was accidentally replaced somehow LOL)
        if state.selection == self.plant:
            pg.draw.rect(surface, (255, 255, 0), (self.x, self.y, self.hitbox_w, self.hitbox_h), 3, border_radius=0)

# Sun Counter
class SunCounter(UI):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0)
    
    def draw(self, surface):
        sun_text = Arial_24_bold.render(str(state.sun), True, (255, 255, 255))
        surface.blit(sun_text, (self.x, self.y))



# --------- lawn ---------

class LawnTile(Button):
    def __init__(self, x, y, hitbox_w, hitbox_h, terrain_type, alt=False):
        super().__init__(x, y, hitbox_w, hitbox_h, "CLICK")
        temp = []
        for i in entities.layers:
            temp.append((i, None))
        self.layers = dict(temp)
        self.platforms = {"land":0,"water":0}
        self.terrain_type = terrain_type
        self.alt = alt
        self.rect = pg.Rect(self.x, self.y, self.hitbox_w, self.hitbox_h)
    
    def is_placement_allowed(self):
        plant = state.selection
        if plant and not state.shovel_active:
            # Check if the target layer is empty
            is_empty_tile = not self.layers[plant.layer]
            
            # Direct terrain match
            is_valid_terrain = self.terrain_type in plant.terrain
            
            # Platform-based support (only if current terrain matches)
            # e.g. plant wants to go on "water", and this tile is "water",
            # so we can check if the platform exists on this specific terrain type
            for i in range(len(state.selection.terrain)):
                is_platform_supported = self.platforms.get(state.selection.terrain[i], 0) > 0
                if is_platform_supported: break
            
            if is_empty_tile and (is_valid_terrain or is_platform_supported):
                return True
        return False
    
    def on_activation(self):
        if self.is_placement_allowed():
            new_plant = state.selection(self.x + self.hitbox_w / 2, self.y + self.hitbox_h / 2)
            new_plant.tile = self  # Assign this tile to the plant
            self.layers[state.selection.layer] = new_plant
            # apply seed packet cooldown
            state.seed_cooldowns[state.seed_packets.index(state.selection)] = state.selection.cooldown
            # deduct sun cost
            state.sun -= state.selection.sun_cost
            platform = getattr(state.selection, "platform_type", [])
            if platform:
                for j in platform:
                    self.platforms[j] += 1
        elif not state.selection and state.shovel_active:
            for i in reversed(entities.layers):
                # "do tomorrow" - ok, doing tomorrow lol ("09/05/2025"-10/05/2025)
                if self.layers[i]: # if something exists here
                    # if this plant is a platform
                    platform = getattr(self.layers[i], "platform_type", [])
                    # empty lists are falsy
                    if platform:
                        for j in platform:
                            self.platforms[j] -= 1 # deduct one from each layer where this platform could otherwise support something
                    entities.Entity.instances.discard(self.layers[i]) # remove the instance of this plant
                    self.layers[i] = None # remove the plant from this tile
                    break
        # even if all checks fail...
        state.shovel_active = False # deactivate
        state.selection = None # deselect
    
    def draw(self, surface):
        if self.terrain_type == "land":
            color = (26, 122, 62) if not self.alt else (89, 193, 53)
            pg.draw.rect(surface, color, self.rect)
        elif self.terrain_type == "water":
            color = (40, 92, 196) if not self.alt else (36, 159, 222)
            pg.draw.rect(surface, color, self.rect)
