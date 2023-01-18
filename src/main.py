import time
import pygame
from pygame.locals import *

pygame.init()

ZOOM = 2
BLOCK_SIZE = 32
B_VEC_X = pygame.Vector2(1, 0.5)
B_VEC_Y = pygame.Vector2(-1, 0.5)


def draw_block(display, x, y, block, height, sprite):
    for i in range(height):
        display.blit(sprite, ((x * (B_VEC_X.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                y * (B_VEC_Y.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2),
                              (x * (B_VEC_X.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                      (y - i * 1.8) * (B_VEC_Y.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + block[1]))


def level_setup(level):
    for i, row in enumerate(level):
        for j, block in enumerate(row):
            row[j] = [row[j], 270 + i * 15 * 5, -15]
            i += 1

    return level


def main():
    # main variables
    window = pygame.display.set_mode((800, 600))
    display = pygame.Surface((window.get_width() / ZOOM, window.get_height() / ZOOM))
    clock = pygame.time.Clock()

    # debug and logic variables
    go = False

    # levels
    tutorial = [[4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    tutorial = level_setup(tutorial)

    # assets and objects
    tutorial_tile = pygame.image.load("assets/sprites/tutorial_tile.png").convert()
    tutorial_tile.set_colorkey((255, 255, 255))

    # main loop variables
    done = False
    last_time = time.perf_counter()

    while not done:

        keys = pygame.key.get_pressed()  # input handler

        # setting up delta time
        dt = time.perf_counter() - last_time
        dt *= 60
        last_time = time.perf_counter()

        # processing logic
        if keys[pygame.K_SPACE]:
            go = True

        display.fill((0, 0, 0))

        # Drawing to the display

        # drawing the level
        y = 0
        for row in tutorial:
            x = 13.5
            for block in row:

                if go:
                    if block[1] > 0:
                        block[1] += block[2] * dt
                    elif block[1] < 0:
                        block[2] = block[1] / 10
                        if block[2] < 1:
                            block[1] = 0
                        block[1] -= block[2] * dt

                if block[0] == 1:
                    draw_block(display, x, y, block, 1, tutorial_tile)
                if block[0] == 2:
                    draw_block(display, x, y, block, 2, tutorial_tile)
                if block[0] == 3:
                    draw_block(display, x, y, block, 3, tutorial_tile)
                if block[0] == 4:
                    draw_block(display, x, y, block, 4, tutorial_tile)
                else:
                    draw_block(display, x, y, block, block[0], tutorial_tile)

                x += 1

            y += 1

        pygame.display.update()

        # event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        surf = pygame.transform.scale(display, (window.get_width(), window.get_height()))
        window.blit(surf, (0, 0))

        pygame.display.set_caption(f"{round(clock.get_fps(), 2)}")
        clock.tick(144)


if __name__ == "__main__":
    main()
    pygame.quit()
