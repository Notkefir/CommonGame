import os
import sys

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
FPS = 60
STEP = 6


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


img_counter = 0
img_counter_attack = 0
img_counter_idle = 0

right_run_frames = [load_image('Run1.png'),
                    load_image('Run2.png'),
                    load_image('Run3.png'),
                    load_image('Run4.png'),
                    load_image('Run5.png'),
                    load_image('Run6.png'),
                    load_image('Run7.png'),
                    load_image('Run8.png')]

left_run_frames = [pygame.transform.flip(image, True, False) for image in right_run_frames]

right_attack_frames = [load_image('Attack1.png'),
                       load_image('Attack2.png'),
                       load_image('Attack3.png'),
                       load_image('Attack4.png'),
                       load_image('Attack5.png'),
                       load_image('Attack6.png')]

left_attack_frames = [pygame.transform.flip(image, True, False) for image in right_attack_frames]

right_idle_frames = [load_image('Idle1.png'),
                     load_image('_dle2.png'),
                     load_image('Idle3.png'),
                     load_image('_dle4.png'),
                     load_image('Idle5.png'),
                     load_image('Idle6.png'),
                     load_image('_dle7.png'),
                     load_image('Idle8.png'),
                     load_image('Idle9.png'),
                     load_image('Idle10.png')]

left_idle_frames = [pygame.transform.flip(image, True, False) for image in right_idle_frames]

def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(sprite_sh_ims, tile_size, level, sprites, tile_groups, tile_images):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # if level[y][x] == '.':
            #     Tile('empty', x, y, tile_groups, sprites, tile_size, tile_images)
            if level[y][x] == '#':
                Tile('wall', x, y, tile_groups, sprites, tile_size, tile_images)
            elif level[y][x] == '@':
                # Tile('empty', x, y, tile_groups, sprites, tile_size, tile_images)
                new_player = Player(x, y, sprite_sh_ims, tile_size, sprites, tile_groups)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_groups, all_sprites, tile_width, tile_images):
        super().__init__(tile_groups[tile_type], all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_width * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tilewidth, all_sprites, tile_groups):
        super().__init__(all_sprites)
        self.walls_group = tile_groups
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * 50
        self.rect.y = y * 50
        self.tile_width = tilewidth
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.r_l = ''
        self.atk = False
        self.in_move = False

    def update(self, *args, **kwargs) -> None:
        self.movements()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        if pygame.sprite.spritecollideany(self, self.walls_group['wall']):
            self.rect.x -= self.x_change
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

    def get_pos(self):
        return self.rect

    def standing_person(self):
        global img_counter_idle

        if (self.facing == 'standing' and self.r_l == 'right') or self.facing == 'standing' and self.r_l == '':
            if img_counter_idle == 40:
                img_counter_idle = 0

            self.image = (right_idle_frames[img_counter_idle // 5])
            img_counter_idle += 1
        if self.r_l == 'left' and self.facing == 'standing':
            if img_counter_idle == 40:
                img_counter_idle = 0
                print(1)

            self.image = (left_idle_frames[img_counter_idle // 5])
            img_counter_idle += 1

    def run_person(self):
        global img_counter

        if self.facing == 'right':
            if img_counter == 40:
                img_counter = 0

            self.image = (right_run_frames[img_counter // 5])
            img_counter += 1
        if self.facing == 'left':
            if img_counter == 40:
                img_counter = 0

            self.image = (left_run_frames[img_counter // 5])
            img_counter += 1


    def attack_person(self):
        global img_counter_attack
        #print(self.atk, self.in_move, self.r_l)

        if self.atk and not self.in_move and self.r_l == '':
            print(1)
            if img_counter_attack == 24:
                img_counter_attack = 0

            self.image = (right_attack_frames[img_counter_attack // 4])
            img_counter_attack += 1

        elif (self.r_l == 'right' and not self.in_move) and self.atk:
            if img_counter_attack == 24:
                img_counter_attack = 0

            self.image = (right_attack_frames[img_counter_attack // 4])
            img_counter_attack += 1
        elif self.r_l == 'left' and self.atk and self.facing == 'standing':
            if img_counter_attack == 24:
                img_counter_attack = 0

            self.image = (left_attack_frames[img_counter_attack // 4])
            img_counter_attack += 1
        self.atk = False



def game():
    fon = pygame.transform.scale(load_image2('fon-game.png'), (800, 600))
    screen.blit(fon, (0, 0))
    tile_images = {
        'wall': load_image2('box.png'),
    }
    # группы спрайтов

    # Player(600, 400)
    sprite_sheet_image = load_image('Run1.png', -1)
    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    # группы спрайтов

    # player_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()

    tile_groups = {
        'wall': walls_group,
    }

    m, level_x, level_y = generate_level(sprite_sheet_image, tile_width, load_level('map.txt'), all_sprites,
                                         tile_groups, tile_images)

    # m = Player(sprite_sheet_image, tile_width, all_sprites)
    running = True
    while running:
        #screen.fill('YELLOW')
        screen.blit(fon, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        m.standing_person()
        m.run_person()
        m.attack_person()
        all_sprites.draw(screen)
        # player_group.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    game()
