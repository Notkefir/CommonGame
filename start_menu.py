import os
import sys
import pygame
from pygame.locals import *
from movement import game

pygame.init()

screen_width = 800
screen_height = 600

VOLUME = '60'

FPS = 60


"""all_sprites нужно будет добавить в функцию и оттуда передавать ее как в файле movement"""
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode((screen_width, screen_height))
"""название нужно будет поменять"""
pygame.display.set_caption('PyGame Project')
BUTTON_CLICK = pygame.mixer.Sound('sounds/button_click.wav')
DIFFICULT = ['easy', 'mid', 'hard']
IND_DIF = 0
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


class Arrow(pygame.sprite.Sprite):
    Arrow_image = load_image('smallarrow.png', -1)

    def __init__(self, *group, pos_x=400, pos_y=400):
        super().__init__(*group)
        self.image = Arrow.Arrow_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 135
        self.v = 2

    def update(self, *args):
        pass

    def get_coords(self):
        return self.rect


m = Arrow(all_sprites)


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (245, 4, 47)
        self.active_color = (53, 204, 200)

    def draw(self, x, y, message, action=None, font_size=50):
        arrow_coords = (m.get_coords()[0], m.get_coords()[1])
        is_clicked = pygame.mouse.get_pressed()

        if y < arrow_coords[1] < y + self.height:
            """нужно поменять display"""
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if pygame.key.get_pressed()[K_RETURN]:
                pygame.mixer.Sound.play(BUTTON_CLICK).set_volume(int(VOLUME) / 100)
                pygame.time.delay(300)
                if action:
                    action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, 'white')

        screen.blit(text, (x + ((self.width - text.get_width()) // 2), y + (self.height - text.get_height()) // 2))


class SystemButton(Button):
    def __init__(self, picture, width, height):
        super().__init__(width, height)
        self.picture = picture

    def draw(self, x, y, message, action=None, font_size=50):
        mouse = pygame.mouse.get_pos()
        mouse_coord_x = mouse[0]
        mouse_coord_y = mouse[1]
        is_clicked = pygame.mouse.get_pressed()

        screen.blit(pygame.transform.scale(load_image(self.picture), (self.width, self.height)), (x, y))
        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, 'white')
        screen.blit(text, (x + 50, y - 5))

        if x < mouse_coord_x < x + self.width and y < mouse_coord_y < y + self.height:
            if is_clicked[0] == 1:
                pygame.mixer.Sound.play(BUTTON_CLICK).set_volume(int(VOLUME) / 100)
                pygame.time.delay(300)
                if action:
                    action()


def text_writter(x, y, text):
    font = pygame.font.Font(None, 50)
    text = font.render(text, True, 'white')
    screen.blit(text, (x, y))


def loud_volume():
    global VOLUME
    VOLUME = int(VOLUME)
    VOLUME += 10
    if VOLUME == 110:
        VOLUME = 0


def quiet_volume():
    global VOLUME
    VOLUME = int(VOLUME)
    VOLUME -= 10
    if VOLUME == 0:
        VOLUME = 100


def up_difficult():
    global IND_DIF
    IND_DIF += 1
    if IND_DIF == 3:
        IND_DIF = 0


def low_difficult():
    global IND_DIF
    IND_DIF -= 1
    if IND_DIF == -1:
        IND_DIF = 2


def game_begin():
    game()
    # fon = pygame.transform.scale(load_image('backgroundfonmenu.jpg'), (screen_width, screen_height))
    # screen.blit(fon, (0, 0))
    # clock = pygame.time.Clock()
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 print(1)
    #                 Menu_start()
    #     pygame.display.flip()
    # pygame.quit()


def settings():
    fon = pygame.transform.scale(load_image('backgroundfonsettings.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    fon = pygame.transform.scale(load_image('wood.png'), (300, 400))
    screen.blit(fon, (250, 50))
    plus_btn = SystemButton('plus.png', 30, 20)
    minus_btn = SystemButton('minus-sign.png', 30, 20)
    left_arrow = SystemButton('left-arrow.png', 30, 20)
    right_arrow = SystemButton('right-arrow.png', 30, 20)
    running = True

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Menu_start()
        screen.blit(fon, (250, 50))
        text_writter(340, 100, 'Volume')
        plus_btn.draw(320, 150, str(VOLUME), loud_volume)
        minus_btn.draw(440, 150, '', quiet_volume)
        text_writter(335, 250, 'Difficult')
        right_arrow.draw(450, 300, '', up_difficult)
        left_arrow.draw(315, 300, DIFFICULT[IND_DIF], low_difficult)
        pygame.display.flip()


def highscore_table():
    fon = pygame.transform.scale(load_image('backgroundfonsettings.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    fon = pygame.transform.scale(load_image('wood.png'), (400, 500))
    screen.blit(fon, (215, 50))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Menu_start()
        pygame.display.flip()


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
        leaderbords_btn.draw(250, 285, 'Leaderboards', highscore_table)
        help_btn.draw(250, 375, 'Help')
        exit_btn.draw(250, 465, 'Exit', terminate)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    Menu_start()
