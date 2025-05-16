import pygame
import math
import time
import random
pygame.init()

times = []
values = [0, 5, 10, 15]

screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

# Create glow sprite
glow = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.circle(glow, (random.choice(values), random.choice(values), random.choice(values), 10), (50, 50), 5)

x = 0
running = True
while running:
    start = time.perf_counter()
    
    x += 1
    
    screen.fill((0, 0, 0))  # black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Additive blend glow effect
    for i in range(10000):
        y_offset = 10 * math.sin(0.05*x+0.05*i)
        screen.blit(glow, (i-200, 100 + y_offset), special_flags=pygame.BLEND_ADD)

    pygame.display.flip()
    
    fps = clock.get_fps()
    pygame.display.set_caption(f"My Cool Game - FPS: {fps:.2f}")
    
    clock.tick(60)
    
    end = time.perf_counter()
    times.append(end - start)
pygame.quit()
print(f"Average time between frames: {sum(times)/len(times):.6f} seconds")