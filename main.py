import time
import pygame
from pygame.locals import *

pygame.init()

ZOOM = 2
window = pygame.display.set_mode((800, 600))
display = pygame.Surface((window.get_width()/ZOOM, window.get_height()/ZOOM))
clock = pygame.time.Clock()


done = False
last_time = time.perf_counter()

while not done:

    keys = pygame.key.get_pressed()

    dt = time.perf_counter() - last_time
    dt *= 60
    last_time = time.perf_counter()

    window.fill((0, 0, 0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    clock.tick(144)


pygame.quit()
