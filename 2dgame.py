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


img_counter = 0

right_run_frames = [load_image('Run1.png'),
                    load_image('Run2.png'),
                    load_image('Run3.png'),
                    load_image('Run4.png'),
                    load_image('Run5.png'),
                    load_image('Run6.png'),
                    load_image('Run7.png'),
                    load_image('Run8.png')]

left_run_frames = [pygame.transform.flip(image, True, False) for image in right_run_frames]


class Player(pygame.sprite.Sprite):
    def __init__(self, image, tilewidth, all_sprites):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.tile_width = tilewidth
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'

    def update(self, *args, **kwargs) -> None:
        self.movements()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0
        # x, y = 0, 0
        # if pygame.key.get_pressed()[K_LEFT]:
        #     x -= self.tile_width * STEP // FPS
        # if pygame.key.get_pressed()[K_RIGHT]:
        #     x += self.tile_width * STEP / FPS
        # if pygame.key.get_pressed()[K_UP]:
        #     y -= self.tile_width * STEP / FPS
        # if pygame.key.get_pressed()[K_DOWN]:
        #     y += self.tile_width * STEP / FPS
        # if self.rect[0] > 1108:
        #     x = -1
        #     self.image = pygame.transform.flip(self.image, True, False)
        # if self.rect[0] <= 0:
        #     x = 1
        # if self.rect[1] > 707:
        #     y = -1
        # if self.rect[1] <= 0:
        #     y = 1
        # self.rect = self.rect.move(x, y)

    def movements(self):
        if pygame.key.get_pressed()[K_LEFT]:
            self.x_change -= self.tile_width * STEP // FPS
            self.facing = 'left'
        if pygame.key.get_pressed()[K_RIGHT]:
            self.x_change += self.tile_width * STEP / FPS
            self.facing = 'right'
        if pygame.key.get_pressed()[K_UP]:
            self.y_change -= self.tile_width * STEP / FPS
            # self.facing = 'up'
        if pygame.key.get_pressed()[K_DOWN]:
            self.y_change += self.tile_width * STEP / FPS
            # self.facing = 'down'
        if self.y_change == 0 and self.x_change == 0:
            self.facing = 'standing'

    def get_pos(self):
        return self.rect

    def run_person(self):
        global img_counter

        if self.facing == 'right':
            x = self.rect.x
            y = self.rect.y
            if img_counter == 40:
                img_counter = 0

            # screen.blit(right_run_frames[img_counter // 5], (x, y))
            self.image = (right_run_frames[img_counter // 5])
            img_counter += 1
        if self.facing == 'left':
            x = self.rect.x
            y = self.rect.y
            if img_counter == 40:
                img_counter = 0

            # screen.blit(left_run_frames[img_counter // 5], (x, y))
            self.image = (left_run_frames[img_counter // 5])
            img_counter += 1

        if self.facing == 'standing':
            x = self.rect.x
            y = self.rect.y
            #screen.blit(load_image('Run5.png'), (x, y))
            self.image = (load_image('Run5.png'))


def game():
    # группы спрайтов

    # Player(600, 400)
    sprite_sheet_image = load_image('Run1.png', -1)
    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    # группы спрайтов

    # player_group = pygame.sprite.Group()

    m = Player(sprite_sheet_image, tile_width, all_sprites)
    running = True
    while running:
        screen.fill('YELLOW')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        m.run_person()
        all_sprites.draw(screen)
        # player_group.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    game()
