import math
import os
import random
import sys

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
FPS = 60
STEP = 6
STEP_ENEMY = 2
TILEWIDTH = 50

new = 0


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('player_sprites', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Spritesheet:
    def __init__(self, file):
        self.sheet = load_image(file)

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey('BLACK')
        return sprite


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites

        super().__init__(self.groups)
        self.tile_width = TILEWIDTH

        self.character_sprite_sheet = Spritesheet('Idles.png')
        self.run_sprite_sheet = Spritesheet('Run.png')
        self.attack_sprite_sheet = Spritesheet('Attack.png')

        self.image = self.character_sprite_sheet.get_sprite(42, 40, 30, 45)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILEWIDTH
        self.rect.y = y * TILEWIDTH

        self.score = 0

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

        self.animation_loop = 0
        self.animation_loop_atk = 0

        self.r_l = ''
        self.atk = False
        self.in_move = False

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies_group, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_portal(self):
        hits = pygame.sprite.spritecollide(self, self.game.portal_group, False)
        if hits:
            self.kill()
            self.game.game_vin()

    def update(self, *args, **kwargs) -> None:
        self.movements()
        self.animate()
        self.collide_enemy()
        self.collide_portal()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        if self.rect.y <= 220:
            self.rect.y -= self.y_change

        self.x_change = 0
        self.y_change = 0

    def movements(self):
        if pygame.key.get_pressed()[K_a]:
            self.x_change -= self.tile_width * STEP / FPS
            self.facing = 'left'
            self.atk = False
            self.in_move = True
            self.r_l = 'left'
        if pygame.key.get_pressed()[K_d]:
            self.x_change += self.tile_width * STEP / FPS
            self.facing = 'right'
            self.atk = False
            self.in_move = True
            self.r_l = 'right'
        if pygame.key.get_pressed()[K_w]:
            self.y_change -= self.tile_width * STEP / FPS
            # self.facing = 'up'
            self.r_l = ''
            self.atk = False
            self.in_move = True
        if pygame.key.get_pressed()[K_s]:
            self.y_change += self.tile_width * STEP / FPS
            # self.facing = 'down'
            self.r_l = ''
            self.atk = False
            self.in_move = True
        if self.y_change == 0 and self.x_change == 0:
            self.facing = 'standing'
            # self.atk = False
            self.in_move = False
        if pygame.mouse.get_pressed()[0]:
            self.atk = True

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls_group, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls_group, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def get_pos(self):
        return self.rect.x, self.rect.y

    def animate(self):
        idle_animations_right = [self.character_sprite_sheet.get_sprite(42, 40, 30, 45),
                                 self.character_sprite_sheet.get_sprite(163, 40, 30, 45),
                                 self.character_sprite_sheet.get_sprite(282, 40, 30, 45),
                                 self.character_sprite_sheet.get_sprite(402, 40, 30, 45),
                                 self.character_sprite_sheet.get_sprite(522, 40, 30, 45),
                                 self.character_sprite_sheet.get_sprite(642, 40, 30, 45),
                                 self.character_sprite_sheet.get_sprite(762, 40, 30, 45),
                                 self.character_sprite_sheet.get_sprite(882, 40, 30, 45),
                                 self.character_sprite_sheet.get_sprite(1002, 40, 30, 45),
                                 self.character_sprite_sheet.get_sprite(1122, 40, 30, 45)]

        idle_animations_left = [pygame.transform.flip(image, True, False) for image in idle_animations_right]

        run_animations_right = [self.run_sprite_sheet.get_sprite(42, 40, 30, 45),
                                self.run_sprite_sheet.get_sprite(163, 40, 30, 45),
                                self.run_sprite_sheet.get_sprite(282, 40, 30, 45),
                                self.run_sprite_sheet.get_sprite(402, 40, 30, 45),
                                self.run_sprite_sheet.get_sprite(522, 40, 30, 45),
                                self.run_sprite_sheet.get_sprite(642, 40, 30, 45),
                                self.run_sprite_sheet.get_sprite(762, 40, 30, 45),
                                self.run_sprite_sheet.get_sprite(882, 40, 30, 45),
                                self.run_sprite_sheet.get_sprite(1002, 40, 30, 45),
                                self.run_sprite_sheet.get_sprite(1122, 40, 30, 45)]

        run_animations_left = [pygame.transform.flip(image, True, False) for image in run_animations_right]

        attack_animations_right = [self.attack_sprite_sheet.get_sprite(40, 40, 40, 45),
                                   self.attack_sprite_sheet.get_sprite(156, 40, 40, 45),
                                   self.attack_sprite_sheet.get_sprite(260, 40, 90, 45),
                                   self.attack_sprite_sheet.get_sprite(380, 40, 69, 45),
                                   self.attack_sprite_sheet.get_sprite(506, 40, 40, 45),
                                   self.attack_sprite_sheet.get_sprite(629, 40, 40, 45)]

        attack_animations_left = [pygame.transform.flip(image, True, False) for image in attack_animations_right]

        if (self.facing == 'standing' and self.r_l == 'right') or self.facing == 'standing' and self.r_l == '':
            self.image = idle_animations_right[math.floor(self.animation_loop // 5)]
            self.animation_loop += 1
            if self.animation_loop >= 40:
                self.animation_loop = 0
        if self.r_l == 'left' and self.facing == 'standing':
            self.image = idle_animations_left[math.floor(self.animation_loop // 5)]
            self.animation_loop += 1
            if self.animation_loop >= 40:
                self.animation_loop = 0

        if self.facing == 'right':
            if self.animation_loop == 40:
                self.animation_loop = 0

            self.image = (run_animations_right[self.animation_loop // 5])
            self.animation_loop += 1
        if self.facing == 'left':
            if self.animation_loop == 40:
                self.animation_loop = 0

            self.image = (run_animations_left[self.animation_loop // 5])
            self.animation_loop += 1

        if self.atk and not self.in_move and self.r_l == '':
            self.image = (attack_animations_right[self.animation_loop_atk // 8])
            self.animation_loop_atk += 1
            if self.animation_loop_atk >= 24:
                self.animation_loop_atk = 0

        elif (self.r_l == 'right' and not self.in_move) and self.atk:
            self.image = (attack_animations_right[self.animation_loop_atk // 8])
            self.animation_loop_atk += 1
            if self.animation_loop_atk >= 24:
                self.animation_loop_atk = 0

        elif self.r_l == 'left' and self.atk and self.facing == 'standing':
            self.image = (attack_animations_left[self.animation_loop_atk // 8])
            self.animation_loop_atk += 1
            if self.animation_loop_atk >= 24:
                self.animation_loop_atk = 0

        self.atk = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(self.game.all_sprites, self.game.enemies_group)

        self.screen = screen

        self.enemy_sprite_sheet_r = Spritesheet('golem.png')
        self.enemy_sprite_sheet_l = Spritesheet('golem.png')

        self.tile_width = TILEWIDTH

        self.image = self.enemy_sprite_sheet_r.get_sprite(2, 8, 40, 42)
        self.rect = self.image.get_rect()
        self.rect.x = x * self.tile_width
        self.rect.y = y * self.tile_width

        self.status = 'friendly'
        self.p_x = 0
        self.p_y = 0

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right', 'down', 'up'])

        self.animation_loop = 0
        self.movement_loop = 0

        self.max_trevel = random.randint(7, 30)

        self.r_l = ''
        self.atk = False
        self.in_move = False

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.rect.x in range(self.p_x - 20, self.p_x + 50) and self.rect.y in range(self.p_y - 20, self.p_y + 65):
            self.status = 'agressive'
        else:
            self.status = 'friendly'
        if self.status == 'friendly':
            if self.facing == 'left':
                self.x_change -= 3
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_trevel:
                    self.facing = 'right'

            if self.facing == 'right':
                self.x_change += 3
                self.movement_loop += 1
                if self.movement_loop >= self.max_trevel:
                    self.facing = 'left'

            if self.facing == 'down':
                self.y_change += 3
                self.movement_loop += 1
                if self.movement_loop >= self.max_trevel:
                    self.facing = 'up'

            if self.facing == 'up':
                self.y_change -= 3
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_trevel:
                    self.facing = 'down'

    def animate(self):
        run_animations_right = [self.enemy_sprite_sheet_r.get_sprite(3, 54, 35, 46),
                                self.enemy_sprite_sheet_r.get_sprite(53, 54, 35, 46),
                                self.enemy_sprite_sheet_r.get_sprite(101, 54, 35, 46)]

        run_animations_left = [self.enemy_sprite_sheet_l.get_sprite(3, 102, 35, 46),
                               self.enemy_sprite_sheet_l.get_sprite(53, 102, 35, 46),
                               self.enemy_sprite_sheet_l.get_sprite(101, 102, 35, 46)]

        run_animations_down = [self.enemy_sprite_sheet_r.get_sprite(2, 6, 44, 46),
                               self.enemy_sprite_sheet_r.get_sprite(51, 6, 44, 46),
                               self.enemy_sprite_sheet_r.get_sprite(98, 6, 44, 46)]

        run_animations_up = [self.enemy_sprite_sheet_r.get_sprite(2, 154, 44, 46),
                             self.enemy_sprite_sheet_r.get_sprite(51, 154, 44, 46),
                             self.enemy_sprite_sheet_r.get_sprite(98, 154, 44, 46)]

        if self.facing == 'left':
            if self.animation_loop == 18:
                self.animation_loop = 0

            self.image = (run_animations_right[self.animation_loop // 6])
            self.animation_loop += 1

        if self.facing == 'right':
            if self.animation_loop == 18:
                self.animation_loop = 0

            self.image = (run_animations_left[self.animation_loop // 6])
            self.animation_loop += 1

        if self.facing == 'up':
            if self.animation_loop == 18:
                self.animation_loop = 0

            self.image = (run_animations_up[self.animation_loop // 6])
            self.animation_loop += 1

        if self.facing == 'down':
            if self.animation_loop == 18:
                self.animation_loop = 0

            self.image = (run_animations_down[self.animation_loop // 6])
            self.animation_loop += 1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(self.game.all_sprites, self.game.walls_group)

        self.x = x * 50
        self.y = y * 50
        self.width = 50
        self.height = 50

        self.wall_sprite = Spritesheet('box.png')
        self.image = self.wall_sprite.get_sprite(0, 0, 50, 50)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(self.game.all_sprites, self.game.portal_group)

        self.x = x * 50
        self.y = y * 50
        self.width = 50
        self.height = 50

        self.portal_sprite = Spritesheet('portal.png')
        self.image = self.portal_sprite.get_sprite(17, 274, 97, 85)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animation_loop = 0

    def update(self):
        self.animate()

    def animate(self):
        portal_animation = [self.portal_sprite.get_sprite(17, 266, 97, 97),
                            self.portal_sprite.get_sprite(142, 266, 97, 97),
                            self.portal_sprite.get_sprite(267, 266, 97, 99),
                            self.portal_sprite.get_sprite(394, 266, 97, 99)]

        if self.animation_loop == 16:
            self.animation_loop = 0

        self.image = (portal_animation[self.animation_loop // 4])
        self.animation_loop += 1
