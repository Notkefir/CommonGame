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
tilewidth = 50

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


def load_image2(name, colorkey=None):
    fullname = os.path.join('data', name)
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


def generate_level(level, sprites, tile_groups, tile_images, enemies):
    new_player, new_enemy, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # if level[y][x] == '.':
            #     Tile('empty', x, y, tile_groups, sprites, tile_size, tile_images)
            if level[y][x] == '#':
                Tile('wall', x, y, tile_groups, sprites, tilewidth, tile_images)
            elif level[y][x] == '@':
                # Tile('empty', x, y, tile_groups, sprites, tile_size, tile_images)
                new_player = Player(x, y, sprites, tile_groups, enemies)
            elif level[y][x] == '%':
                new_enemy = Enemy(x, y, sprites, tile_groups, enemies)
    # вернем игрока, а также размер поля в клетках
    return new_player, new_enemy


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_groups, all_sprites, tile_width, tile_images):
        super().__init__(tile_groups[tile_type], all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_width * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, tile_groups, enemies):
        super().__init__(all_sprites)
        self.walls_group = tile_groups
        self.enemies_group = enemies
        self.tile_width = tilewidth
        self.character_sprite_sheet = Spritesheet('Idles.png')
        self.run_sprite_sheet = Spritesheet('Run.png')
        self.attack_sprite_sheet = Spritesheet('Attack.png')
        self.image = self.character_sprite_sheet.get_sprite(42, 40, 30, 45)
        self.rect = self.image.get_rect()
        self.rect.x = x * 50
        self.rect.y = y * 50
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 0
        self.animation_loop_atk = 0
        self.r_l = ''
        self.atk = False
        self.in_move = False

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.enemies_group, False)
        if hits:
            self.kill()
            terminate()

    def update(self, *args, **kwargs) -> None:
        self.movements()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        if pygame.sprite.spritecollideany(self, self.walls_group['wall']):
            self.rect.x -= self.x_change
            self.rect.y -= self.y_change
        if self.rect.y <= 220:
            self.rect.y -= self.y_change

        self.x_change = 0
        self.y_change = 0

    def movements(self):
        if pygame.key.get_pressed()[K_a]:
            self.x_change -= self.tile_width * STEP // FPS
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
        # if pygame.key.get_pressed()[K_SPACE] and not self.in_move:
        #     self.atk = True
        if pygame.mouse.get_pressed()[0]:
            self.atk = True

    @property
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
            if self.animation_loop_atk == 24:
                self.animation_loop_atk = 0

            self.image = (attack_animations_right[self.animation_loop_atk // 6])
            self.animation_loop_atk += 1

        elif (self.r_l == 'right' and not self.in_move) and self.atk:
            if self.animation_loop_atk == 24:
                self.animation_loop_atk = 0

            self.image = (attack_animations_right[self.animation_loop_atk // 6])
            self.animation_loop_atk += 1
        elif self.r_l == 'left' and self.atk and self.facing == 'standing':
            if self.animation_loop_atk == 24:
                self.animation_loop_atk = 0

            self.image = (attack_animations_left[self.animation_loop_atk // 6])
            self.animation_loop_atk += 1
        self.atk = False

    #
    # def attack_person(self):
    #     global img_counter_attack
    #     # print(self.atk, self.in_move, self.r_l)
    #
    # if self.atk and not self.in_move and self.r_l == '':
    #     if img_counter_attack == 24:
    #         img_counter_attack = 0
    #
    #     self.image = (right_attack_frames[img_counter_attack // 4])
    #     img_counter_attack += 1
    #
    # elif (self.r_l == 'right' and not self.in_move) and self.atk:
    #     if img_counter_attack == 24:
    #         img_counter_attack = 0
    #
    #     self.image = (right_attack_frames[img_counter_attack // 4])
    #     img_counter_attack += 1
    # elif self.r_l == 'left' and self.atk and self.facing == 'standing':
    #     if img_counter_attack == 24:
    #         img_counter_attack = 0
    #
    #     self.image = (left_attack_frames[img_counter_attack // 4])
    #     img_counter_attack += 1
    # self.atk = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, tile_groups, enemies_group):
        super().__init__(all_sprites, enemies_group)
        self.screen = screen
        self.walls_group = tile_groups
        self.enemies_group = enemies_group
        self.enemy_sprite_sheet_r = Spritesheet('golem.png')
        self.enemy_sprite_sheet_l = Spritesheet('golem.png')
        self.image = self.enemy_sprite_sheet_r.get_sprite(2, 8, 40, 42)
        self.rect = self.image.get_rect()
        self.rect.x = x * 50
        self.rect.y = y * 50
        self.tile_width = tilewidth
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


def game():
    fon = pygame.transform.scale(load_image2('fon-game.png'), (800, 600))
    screen.blit(fon, (0, 0))
    tile_images = {
        'wall': load_image2('box.png'),
    }
    # группы спрайтов

    all_sprites = pygame.sprite.Group()
    # группы спрайтов

    walls_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()

    tile_groups = {
        'wall': walls_group,
    }

    m, new_enemy = generate_level(load_level('map.txt'), all_sprites,
                                  tile_groups, tile_images, enemies_group)

    x, y = m.get_pos

    # m = Player(sprite_sheet_image, tile_width, all_sprites)
    running = True
    while running:
        screen.blit(fon, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        # player_group.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    game()
