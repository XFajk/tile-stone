import time
import pygame
from pygame.locals import *

pygame.init()

ZOOM = 2
BLOCK_SIZE = 32
B_VEC_X = pygame.Vector2(1, 0.5)
B_VEC_Y = pygame.Vector2(-1, 0.5)


def level_setup(row):
    for i, block in enumerate(row):
        row[i] = [row[i], 270 + i * 30, -5]

    return row


def main():
    # main variables
    window = pygame.display.set_mode((800, 600))
    display = pygame.Surface((window.get_width() / ZOOM, window.get_height() / ZOOM))
    clock = pygame.time.Clock()

    # debug and logic variables
    go = False

    # levels
    tutorial = [[4, 4, 3, 2, 2, 2, 2, 2, 2, 2, 4],
                [4, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1],
                [3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    tutorial = list(map(level_setup, tutorial))
    print(list(tutorial))
    # tutorial = list(map(lambda arg1: list(map(lambda arg2: [arg2, 268, 0.1], arg1)), tutorial))

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
                        block[1] += block[2]*dt
                    else:
                        block[1] = 0

                if block[0] == 1:
                    display.blit(tutorial_tile, ((x * (B_VEC_X.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                            y * (B_VEC_Y.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2),
                                                 (x * (B_VEC_X.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                                         (y - 0) * (
                                                            B_VEC_Y.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + block[1]))
                if block[0] == 2:
                    for i in range(2):
                        display.blit(tutorial_tile, ((x * (B_VEC_X.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                y * (B_VEC_Y.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2),
                                                     (x * (B_VEC_X.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                                             (y - i * 1.8) * (
                                                                B_VEC_Y.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + block[1]))
                if block[0] == 3:
                    for i in range(3):
                        display.blit(tutorial_tile, ((x * (B_VEC_X.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                y * (B_VEC_Y.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2),
                                                     (x * (B_VEC_X.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                                             (y - i * 1.8) * (
                                                                B_VEC_Y.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + block[1]))
                if block[0] == 4:
                    for i in range(4):
                        display.blit(tutorial_tile, ((x * (B_VEC_X.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                y * (B_VEC_Y.x * BLOCK_SIZE / 2) - BLOCK_SIZE / 2),
                                                     (x * (B_VEC_X.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + (
                                                             (y - i * 1.8) * (
                                                                B_VEC_Y.y * BLOCK_SIZE / 2) - BLOCK_SIZE / 2) + block[1]))

                x += 1

            y += 1

        pygame.display.update()

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
