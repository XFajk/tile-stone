import pygame

BS = 32
I_VEC = pygame.Vector2(1, 0.5)
J_VEC = pygame.Vector2(-1, 0.5)


def generate_animation_frames(path: str, name: str, number_of_frames: int, distribution: list) -> list:
    animation_frames = []
    for i in range(number_of_frames):
        full_path = path+name+str(i)+".png"
        for j in range(distribution[i]):
            img = pygame.image.load(full_path).convert()
            img.set_colorkey((255, 255, 255))
            animation_frames.append(img)

    return animation_frames


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/player/player_tile0.png")
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()

        self.pos = pygame.Vector2(0, 0)
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        self.animation_frames = generate_animation_frames("assets/sprites/player/", "player_tile", 11, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5])
        self.animation_index = 0
        self.animation_flow = 0

        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def update(self, dt, x, y, block, level, idx, keys) -> None:

        self.animation_frames = generate_animation_frames("assets/sprites/player/", "player_tile", 11, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5])

        # (reminder change the player animation)
        # Movement logic begin
        if keys[pygame.K_d] and not self.left and not self.up and not self.down:
            if not self.right and level[idx[0]][idx[1] + 1][0] != 3 or level[idx[0]][idx[1] + 1][3] == 1:
                self.animation_flow = 1
            self.right = True

        if keys[pygame.K_a] and not self.right and not self.up and not self.down:
            if not self.left and level[idx[0]][idx[1]-1][0] != 3 or level[idx[0]][idx[1]-1][3] == 1:
                self.animation_flow = 1
            self.left = True

        if keys[pygame.K_w] and not self.down and not self.right and not self.left:
            if not self.up and level[idx[0]-1][idx[1]][0] != 3 or level[idx[0]-1][idx[1]][3] == 1:
                self.animation_flow = 1
            self.up = True

        if keys[pygame.K_s] and not self.up and not self.right and not self.left:
            if not self.down and level[idx[0]+1][idx[1]][0] != 3 or level[idx[0]+1][idx[1]][3] == 1:
                self.animation_flow = 1
            self.down = True

        if self.right:
            self.animation_index += self.animation_flow
            if self.animation_index == len(self.animation_frames)-1:
                level[idx[0]][idx[1]][5] = False
                self.animation_flow = -1
                try:
                    if level[idx[0]][idx[1]+1][0] != 3 or level[idx[0]][idx[1]+1][3] == 1:
                        level[idx[0]][idx[1]+1][5] = True
                    else:
                        level[idx[0]][idx[1]][5] = True
                except IndexError:
                    level[idx[0]][idx[1]][5] = True
            if self.animation_index <= 0:
                self.animation_flow = 0
            if self.animation_flow == 0:
                self.right = False

        if self.left:
            self.animation_index += self.animation_flow
            if self.animation_index == len(self.animation_frames)-1:
                level[idx[0]][idx[1]][5] = False
                self.animation_flow = -1
                try:
                    if level[idx[0]][idx[1]-1][0] != 3 or level[idx[0]][idx[1]-1][3] == 1:
                        level[idx[0]][idx[1]-1][5] = True
                    else:
                        level[idx[0]][idx[1]][5] = True
                except IndexError:
                    level[idx[0]][idx[1]][5] = True
            if self.animation_index <= 0:
                self.animation_flow = 0
            if self.animation_flow == 0:
                self.left = False

        if self.down:
            self.animation_index += self.animation_flow
            if self.animation_index == len(self.animation_frames)-1:
                level[idx[0]][idx[1]][5] = False
                self.animation_flow = -1
                try:
                    if level[idx[0]+1][idx[1]][0] != 3 or level[idx[0]+1][idx[1]][3] == 1:
                        level[idx[0]+1][idx[1]][5] = True
                    else:
                        level[idx[0]][idx[1]][5] = True
                except IndexError:
                    level[idx[0]][idx[1]][5] = True
            if self.animation_index <= 0:
                self.animation_flow = 0
            if self.animation_flow == 0:
                self.down = False

        if self.up:
            self.animation_index += self.animation_flow
            if self.animation_index == len(self.animation_frames)-1:
                level[idx[0]][idx[1]][5] = False
                self.animation_flow = -1
                try:
                    if level[idx[0]-1][idx[1]][0] != 3 or level[idx[0]-1][idx[1]][3] == 1:
                        level[idx[0]-1][idx[1]][5] = True
                    else:
                        level[idx[0]][idx[1]][5] = True
                except IndexError:
                    level[idx[0]][idx[1]][5] = True
            if self.animation_index <= 0:
                self.animation_flow = 0
            if self.animation_flow == 0:
                self.up = False

        # Movement logic end

        self.image = self.animation_frames[self.animation_index]
        self.pos.x = ((x * (I_VEC.x * BS / 2) - BS / 2) + (y * (J_VEC.x * BS / 2)))
        self.pos.y = ((x * (I_VEC.y * BS / 2)) + ((y + block[3] - 3.2) * (J_VEC.y * BS / 2)) + block[1])
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
