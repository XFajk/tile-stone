import random
import time
import pygame
import os
import csv
from pygame.locals import *

pygame.init()

ZOOM = 2
BS = 32
I_VEC = pygame.Vector2(1, 0.5)
J_VEC = pygame.Vector2(-1, 0.5)


def read_csv(filename):
    level = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            level.append(list(row))

    return level


def invert_metrix(a, b, c, d):
    det = 1 / (a*d - b*c)  # determinant

    return {
        "a": det * d,
        "b": det * -b,
        "c": det * -c,
        "d": det * a
    }


def to_grid_cords(pos: pygame.Vector2):
    a = I_VEC.x * BS / 2
    b = J_VEC.x * BS / 2
    c = I_VEC.y * BS / 2
    d = J_VEC.y * BS / 2

    inv = invert_metrix(a, b, c, d)

    return pygame.Vector2(
        x=pos.x * inv["a"] + pos.y * inv["b"],
        y=pos.x * inv["c"] + pos.y * inv["d"]
    )


def draw_block(display, x, y, block, sprite, y_offset=0.0):
    for i in range(block[4]):
        display.blit(sprite, ((x * (I_VEC.x * BS / 2) - BS / 2) + (y * (J_VEC.x * BS / 2)),
                              (x * (I_VEC.y * BS / 2)) + ((y - i * 1.8 + block[3] + y_offset) * (J_VEC.y * BS / 2)) + block[1]))


def level_setup(layout, height):
    for i, row in enumerate(height):
        for j, block in enumerate(row):
            row[j] = int(row[j])+1

    for i, row in enumerate(layout):
        for j, block in enumerate(row):
            if int(row[j]) == 0:
                row[j] = [int(row[j]), 270 + random.randint(1, 20) * 15 * 5, -15, 0.0, height[i][j], True]
            else:
                row[j] = [int(row[j]), 270 + random.randint(1, 20) * 15 * 5, -15, 0.0, height[i][j], False]

    return layout


def main():
    # main variables
    window = pygame.display.set_mode((830, 600))
    display = pygame.Surface((window.get_width() / ZOOM, window.get_height() / ZOOM))
    clock = pygame.time.Clock()

    # debug and logic variables
    go = False

    # levels
    tutorial_type = read_csv("assets/csv/tutorial_type layer.csv")
    tutorial_height = read_csv("assets/csv/tutorial_height layer.csv")
    tutorial = level_setup(tutorial_type, tutorial_height)

    # assets and objects
    tutorial_tile = pygame.image.load("assets/sprites/tutorial_tile.png").convert()
    tutorial_tile.set_colorkey((255, 255, 255))
    no_go_tile = pygame.image.load("assets/sprites/no_go_tile.png").convert()
    no_go_tile.set_colorkey((255, 255, 255))
    start_tile = pygame.image.load("assets/sprites/start_tile.png").convert()
    start_tile.set_colorkey((255, 255, 255))
    end_tile = pygame.image.load("assets/sprites/end_tile.png").convert()
    end_tile.set_colorkey((255, 255, 255))

    player_img = pygame.image.load("assets/sprites/player/player_tile.png").convert()
    player_img.set_colorkey((255, 255, 255))

    # main loop variables
    done = False
    last_time = time.perf_counter()

    while not done:

        keys = pygame.key.get_pressed()  # input handler
        cell_pos = to_grid_cords(
            pos=pygame.Vector2(pygame.mouse.get_pos()[0]/ZOOM, pygame.mouse.get_pos()[1]/ZOOM)
        )
        block_pos = pygame.Vector2(0, 0)

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
        y = -1
        for row in tutorial:
            x = 12
            for block in row:

                if go:
                    if block[1] > 0:
                        block[1] += block[2] * dt
                    elif block[1] < 0:
                        block[2] = block[1] / 10
                        if block[2] < 1:
                            block[1] = 0
                        block[1] -= block[2] * dt

                if int(cell_pos.x) == x and int(cell_pos.y) == y and block[4] == 1:
                    block[3] = -0.2
                    block_pos = pygame.Vector2(x, y)
                else:
                    block[3] = 0.0

                match block[0]:
                    case 0:
                        draw_block(display, x, y, block, start_tile)
                    case 1:
                        draw_block(display, x, y, block, end_tile)
                    case 2:
                        draw_block(display, x, y, block, tutorial_tile)
                    case 3:
                        draw_block(display, x, y, block, no_go_tile)
                    case 4:
                        draw_block(display, x, y, block, tutorial_tile)
                    case _:
                        draw_block(display, x, y, block, tutorial_tile)

                if block[5]:
                    draw_block(display, x, y, block, player_img, -3.2)

                x += 1

            y += 1

        pygame.display.update()

        # event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        surf = pygame.transform.scale(display, (window.get_width(), window.get_height()))
        window.blit(surf, (0, 0))

        pygame.display.set_caption(f"{int(cell_pos.x)} : {int(cell_pos.y)} | {block_pos.x} : {block_pos.y}")
        clock.tick(144)


if __name__ == "__main__":
    main()
    pygame.quit()
