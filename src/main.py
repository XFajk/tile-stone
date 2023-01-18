import random
import time
import pygame
from pygame.locals import *

pygame.init()

ZOOM = 2
BLOCK_SIZE = 32
BLOCK_VECTOR_X = pygame.Vector2(1, 0.5)
BLOCK_VECTOR_Y = pygame.Vector2(-1, 0.5)


def main():
    # main variables
    window = pygame.display.set_mode((800, 600))
    display = pygame.Surface((window.get_width() / ZOOM, window.get_height() / ZOOM))
    clock = pygame.time.Clock()

    # debug and logic variables
    timer = time.perf_counter()

    # levels
    tutorial = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    tutorial = list(map(lambda arg1: list(map(lambda arg2: [arg2, random.randint(1, 10)/10, 0.05], arg1)), tutorial))

    # assets and objects
    tutorial_tile = pygame.image.load("assets/sprites/tutorial_tile.png").convert()
    tutorial_tile.set_colorkey((255, 255, 255))

    # main loop variables
    done = False
    last_time = time.perf_counter()

    while not done:

        keys = pygame.key.get_pressed()


        dt = time.perf_counter() - last_time
        dt *= 60
        last_time = time.perf_counter()

        # processing logic

        display.fill((0, 0, 0))

        # Drawing to the display

        # drawing the level
        y = 0
        for row in tutorial:
            x = 13
            for block in row:
                if block[0] == 1:
                    block[1] += block[2] * dt 
                    if round(block[1], 2) >= 2:
                        block[2] *= -1
                    elif round(block[1], 2) <= -2:
                        block[2] *= -1
                    display.blit(tutorial_tile, ((x * (BLOCK_VECTOR_X.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                y * (BLOCK_VECTOR_Y.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2),
                                                 (x * (BLOCK_VECTOR_X.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                                             (y - block[1]) * (
                                                                 BLOCK_VECTOR_Y.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2)))

                x += 1

            y += 1

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        surf = pygame.transform.scale(display, (window.get_width(), window.get_height()))
        window.blit(surf, (0, 0))
        clock.tick(144)


if __name__ == "__main__":
    main()
    pygame.quit()
