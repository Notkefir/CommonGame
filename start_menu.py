import os
import sys

import pygame

pygame.init()

screen_width = 800
screen_height = 600

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


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (245, 4, 47)
        self.active_color = (53, 204, 200)

    def draw(self, x, y, message, action=None, font_size=50):
        mouse = pygame.mouse.get_pos()
        mouse_coord_x = mouse[0]
        mouse_coord_y = mouse[1]
        is_clicked = pygame.mouse.get_pressed()

        if x < mouse_coord_x < x + self.width and y < mouse_coord_y < y + self.height:
            """нужно поменять display"""
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if is_clicked[0] == 1:
                pygame.mixer.Sound.play(BUTTON_CLICK)
                pygame.time.delay(300)
                if action:
                    action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

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
                    menu_start()
        pygame.display.flip()
    pygame.quit()


def menu_start():
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        start_btn.draw(250, 105, 'Start', game_begin)
        settings_btn.draw(250, 195, 'Settings')
        leaderbords_btn.draw(250, 285, 'Leaderboards')
        help_btn.draw(250, 375, 'Help')
        exit_btn.draw(250, 465, 'Exit', terminate)
        tick = clock.tick()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    menu_start()
