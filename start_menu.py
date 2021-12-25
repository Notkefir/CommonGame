import os
import sys
import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 600

FPS = 60
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode((screen_width, screen_height))
"""название нужно будет поменять"""
pygame.display.set_caption('PyGame Project')
BUTTON_CLICK = pygame.mixer.Sound('sounds/button_click.wav')

"""сюда нужно добавить звуковое сопровождение разных действий"""


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Player(pygame.sprite.Sprite):
    player_image = load_image('smallarrow.png', -1)

    def __init__(self, *group, pos_x=400, pos_y=400):
        super().__init__(*group)
        self.image = Player.player_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 135
        self.v = 2

    def update(self, *args):
        pass

    #     x = y = 0
    #     if pygame.key.get_pressed()[K_UP]:
    #         y -= 20
    #     if pygame.key.get_pressed()[K_DOWN]:
    #         y += 20
    #     self.rect = self.rect.move(x, y)
    #     if self.rect[1] >= 535:
    #         self.rect = self.rect.move(x, -400)
    #     if self.rect[1] <= 90:
    #         self.rect = self.rect.move(x, 400)
    #
    def get_coords(self):
        return self.rect
    #
    # def draw_cursor(self):
    #     screen.blit(self.image, [self.rect.x, self.rect.y])
    #
    # def blit_screen(self):
    #     pygame.display.update()


m = Player(all_sprites)


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (245, 4, 47)
        self.active_color = (53, 204, 200)

    def draw(self, x, y, message, action=None, font_size=50):
        arrow_coords = (m.get_coords()[0], m.get_coords()[1])
        mouse = pygame.mouse.get_pos()
        # mouse_coord_x = mouse[0]
        # mouse_coord_y = mouse[1]
        is_clicked = pygame.mouse.get_pressed()

        if y < arrow_coords[1] < y + self.height:
            """нужно поменять display"""
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if pygame.key.get_pressed()[K_RETURN]:
                pygame.mixer.Sound.play(BUTTON_CLICK)
                pygame.time.delay(300)
                if action:
                    action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, 'white')

        screen.blit(text, (x + ((self.width - text.get_width()) // 2), y + (self.height - text.get_height()) // 2))

class SystemButton:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, message, action=None, font_size=50):
        mouse = pygame.mouse.get_pos()
        mouse_coord_x = mouse[0]
        mouse_coord_y = mouse[1]
        is_clicked = pygame.mouse.get_pressed()

        if x < mouse_coord_x < x + self.width and y < mouse_coord_y < y + self.height:
            """нужно поменять display"""

            if is_clicked[0] == 1:
                pygame.mixer.Sound.play(BUTTON_CLICK)
                pygame.time.delay(300)
                if action:
                    action()

        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, 'white')

        screen.blit(text, (x + ((self.width - text.get_width()) // 2), y + (self.height - text.get_height()) // 2))


def game_begin():
    fon = pygame.transform.scale(load_image('backgroundfonmenu.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))

    running = True

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Menu_start()
        pygame.display.flip()
    pygame.quit()


def settings():
    fon = pygame.transform.scale(load_image('backgroundfonsettings.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    fon = pygame.transform.scale(load_image('wood.png'), (300, 400))
    screen.blit(fon, (250, 50))
    running = True

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Menu_start()
        pygame.display.flip()
    pygame.quit()


def Menu_start():
    fon = pygame.transform.scale(load_image('backgroundfonmenu.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    start_btn = Button(300, 70)
    settings_btn = Button(300, 70)
    leaderbords_btn = Button(300, 70)
    help_btn = Button(300, 70)
    exit_btn = Button(300, 70)
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    m.rect.y -= 90
                    if m.rect.y <= 120:
                        m.rect.y = 500
                if event.key == pygame.K_DOWN:
                    m.rect.y += 90
                    if m.rect.y >= 535:
                        m.rect.y = 135
        start_btn.draw(250, 105, 'Start', game_begin)
        settings_btn.draw(250, 195, 'Settings', settings)
        leaderbords_btn.draw(250, 285, 'Leaderboards')
        help_btn.draw(250, 375, 'Help')
        exit_btn.draw(250, 465, 'Exit', terminate)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    Menu_start()
