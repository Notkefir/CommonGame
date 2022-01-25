import sqlite3
from all_mobs import *

con = sqlite3.connect('database/scores.db')
cur = con.cursor()
pygame.init()

screen_width = 800
screen_height = 600
img_counter_idle = 40
VOLUME = '60'
SCORE = 0
ENEMIES_COUNT = 0

NAME = ''

FPS = 60

all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Warrior Coomarrior')
BUTTON_CLICK = pygame.mixer.Sound('sounds/button_click.wav')
KILL_SOUND = pygame.mixer.Sound('sounds/silnyiy-zamah-i-razrez-popolam.wav')

DIFFICULT = ['easy', 'mid', 'hard']

MAPS = {
    'easy': 'maps/map.txt',
    'mid': 'maps/mid.txt',
    'hard': 'maps/hard.txt'
}

IND_DIF = 0


def load_image(name, colorkey=None):
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


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Arrow(pygame.sprite.Sprite):
    Arrow_image = load_image('smallarrow.png', -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Arrow.Arrow_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 135
        self.v = 2

    def get_coords(self):
        return self.rect


arrow = Arrow(all_sprites)


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (245, 4, 47)
        self.active_color = (53, 204, 200)

    def draw(self, x, y, message, action=None, font_size=50):
        arrow_coords = (arrow.get_coords()[0], arrow.get_coords()[1])

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
        self.mouse = pygame.mouse.get_pos()
        self.mouse_coord_x = self.mouse[0]
        self.mouse_coord_y = self.mouse[1]
        self.is_clicked = pygame.mouse.get_pressed()

    def draw(self, x, y, message, action=None, font_size=50):
        self.mouse = pygame.mouse.get_pos()
        self.mouse_coord_x = self.mouse[0]
        self.mouse_coord_y = self.mouse[1]
        self.is_clicked = pygame.mouse.get_pressed()
        if self.picture != '':
            screen.blit(pygame.transform.scale(load_image(self.picture), (self.width, self.height)), (x, y))
            font = pygame.font.Font(None, font_size)
            text = font.render(message, True, 'white')
            screen.blit(text, (x + 50, y - 5))

            if x < self.mouse_coord_x < x + self.width and y < self.mouse_coord_y < y + self.height:
                if self.is_clicked[0] == 1:
                    pygame.mixer.Sound.play(BUTTON_CLICK).set_volume(int(VOLUME) / 100)
                    pygame.time.delay(300)
                    if action:
                        action()
        else:
            if y < self.mouse_coord_y < y + self.height and x < self.mouse_coord_x < x + self.width:
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
                if self.is_clicked[0] == 1:
                    pygame.mixer.Sound.play(BUTTON_CLICK).set_volume(int(VOLUME) / 100)
                    pygame.time.delay(300)
                    if action:
                        action()

            else:
                pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

            font = pygame.font.Font(None, font_size)
            text = font.render(message, True, 'white')

            screen.blit(text, (x + ((self.width - text.get_width()) // 2), y + (self.height - text.get_height()) // 2))

    def is_pressed(self):
        self.mouse = pygame.mouse.get_pos()
        self.mouse_coord_x = self.mouse[0]
        self.mouse_coord_y = self.mouse[1]
        self.is_clicked = pygame.mouse.get_pressed()
        if (300 < self.mouse_coord_x < 300 + self.width) and (225 < self.mouse_coord_y < 225 + self.height):
            if self.is_clicked[0]:
                return True
            return False
        return False


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
    global SCORE
    SCORE = 0
    g = Start()
    g.new()
    while g.running:
        g.main()
        g.game_over()

    terminate()


def start():
    global NAME
    fon = pygame.transform.scale(load_image('backgroundfonsettings.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))

    left_arrow = SystemButton('left-arrow.png', 30, 20)
    right_arrow = SystemButton('right-arrow.png', 30, 20)
    choose_btn = SystemButton('', 200, 70)

    name_rect = pygame.Rect(300, 400, 200, 65)
    active = False
    name = ''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_start()
                if event.key == pygame.K_BACKSPACE:
                    active = True
                    name = name[:-1]
                else:
                    if active:
                        if len(name) < 8:
                            if event.unicode.isalpha() or event.unicode.isdigit():
                                name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if name_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
        screen.blit(fon, (250, 50))

        pygame.draw.rect(screen, 'BLACK', name_rect, 2)
        text_writter(307, 420, name)

        text_writter(335, 250, 'Difficult')

        right_arrow.draw(450, 300, '', up_difficult)
        left_arrow.draw(315, 300, DIFFICULT[IND_DIF], low_difficult)
        if name:
            if choose_btn.is_pressed():
                NAME = name
                players_in_bd = [str(i[0]) for i in cur.execute(f"SELECT name from player").fetchall()]
                length = len(players_in_bd) + 1
                cur.execute(f"""INSERT INTO player(name) VALUES('{name}')""")
                cur.execute(f"""INSERT INTO scores(id, player_id) VALUES({length}, {length}) """)
                con.commit()
            choose_btn.draw(300, 225, 'CHOOSE', game_begin)

        pygame.display.flip()


def settings():
    fon = pygame.transform.scale(load_image('backgroundfonsettings.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    fon = pygame.transform.scale(load_image('wood.png'), (300, 400))
    screen.blit(fon, (250, 50))
    plus_btn = SystemButton('plus.png', 30, 20)
    minus_btn = SystemButton('minus-sign.png', 30, 20)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_start()
        screen.blit(fon, (250, 50))
        text_writter(340, 100, 'Volume')
        plus_btn.draw(320, 150, str(VOLUME), loud_volume)
        minus_btn.draw(440, 150, '', quiet_volume)
        text_writter(335, 250, 'Difficult')
        pygame.display.flip()


def highscore_table():
    fon = pygame.transform.scale(load_image('backgroundfonsettings.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    fon = pygame.transform.scale(load_image('wood.png'), (400, 600))
    screen.blit(fon, (215, 50))

    y_i = [150]

    score_information = cur.execute(
        f"""SELECT score, player.name from scores,
             player WHERE player.id == player_id ORDER BY score""").fetchall()[
                        ::-1]

    for i in range(len(score_information)):
        y_i.append(y_i[-1] + 60)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_start()
        text_writter(270, 80, 'Name')
        text_writter(420, 80, 'Score')
        for i in range(len(score_information)):
            text_writter(290, y_i[i], str(score_information[i][1]))
            text_writter(440, y_i[i], str(score_information[i][0]))
        pygame.display.flip()


def menu_start():
    fon = pygame.transform.scale(load_image('backgroundfonmenu.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    start_btn = Button(300, 70)
    settings_btn = Button(300, 70)
    leaderbords_btn = Button(300, 70)
    help_btn = Button(300, 70)
    exit_btn = Button(300, 70)
    running = True
    clock_ = pygame.time.Clock()
    while running:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    arrow.rect.y -= 90
                    if arrow.rect.y <= 120:
                        arrow.rect.y = 500
                if event.key == pygame.K_DOWN:
                    arrow.rect.y += 90
                    if arrow.rect.y >= 535:
                        arrow.rect.y = 135
        start_btn.draw(250, 105, 'Start', start)
        settings_btn.draw(250, 195, 'Settings', settings)
        leaderbords_btn.draw(250, 285, 'Leaderboards', highscore_table)
        help_btn.draw(250, 375, 'Help')
        exit_btn.draw(250, 465, 'Exit', terminate)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock_.tick(FPS)
    pygame.quit()


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        super().__init__(self.game.all_sprites, self.game.attacks_group)

        self.score = 0

        self.x = x
        self.y = y

        self.animation_loop = 0

        self.attack_sprite_sheet = Spritesheet('attackwave.png')
        self.image = self.attack_sprite_sheet.get_sprite(0, 0, 32, 32)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        global SCORE, ENEMIES_COUNT
        hits = pygame.sprite.spritecollide(self, self.game.enemies_group, True)
        if hits:
            SCORE += 5
            ENEMIES_COUNT -= 1

    def scores(self):
        return self.score

    def animate(self):
        r_l = self.game.player.r_l

        attack_animations_right = [self.attack_sprite_sheet.get_sprite(0, 64, 32, 32),
                                   self.attack_sprite_sheet.get_sprite(32, 64, 32, 32),
                                   self.attack_sprite_sheet.get_sprite(64, 64, 32, 32),
                                   self.attack_sprite_sheet.get_sprite(96, 64, 32, 32),
                                   self.attack_sprite_sheet.get_sprite(128, 64, 32, 32)]

        attack_animations_left = [self.attack_sprite_sheet.get_sprite(0, 96, 32, 32),
                                  self.attack_sprite_sheet.get_sprite(32, 96, 32, 32),
                                  self.attack_sprite_sheet.get_sprite(64, 96, 32, 32),
                                  self.attack_sprite_sheet.get_sprite(96, 96, 32, 32),
                                  self.attack_sprite_sheet.get_sprite(128, 96, 32, 32)]

        if r_l == '' or r_l == 'right':
            self.image = (attack_animations_right[self.animation_loop // 6])
            self.animation_loop += 1
            if self.animation_loop >= 24:
                self.kill()

        if r_l == 'left':
            self.image = (attack_animations_left[self.animation_loop // 6])
            self.animation_loop += 1
            if self.animation_loop >= 24:
                self.kill()


class Start:
    def __init__(self):
        pygame.init()
        self.fon = pygame.transform.scale(load_image('fon-game.png'), (800, 600))
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.playing = None
        self.all_sprites = None
        self.walls_group = None
        self.enemies_group = None
        self.attacks_group = None
        self.portal_group = None
        self.player = None

    def createtilemap(self):
        global ENEMIES_COUNT
        for i, row in enumerate(load_level(MAPS[DIFFICULT[IND_DIF]])):
            for j, column in enumerate(row):
                if column == '#':
                    Block(self, j, i)
                if column == '@':
                    self.player = Player(self, j, i)
                if column == '%':
                    ENEMIES_COUNT += 1
                    Enemy(self, j, i)
                if column == '&':
                    Portal(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.Group()
        self.walls_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.attacks_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()

        self.createtilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if self.player.r_l == 'right' or self.player.r_l == '':
                    KILL_SOUND.play(0).set_volume(int(VOLUME) / 100)
                    Attack(self, self.player.rect.x + 30, self.player.rect.y)
                if self.player.r_l == 'left':
                    KILL_SOUND.play(0).set_volume(int(VOLUME) / 100)
                    Attack(self, self.player.rect.x - 30, self.player.rect.y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_start()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.blit(self.fon, (0, 0))
        self.all_sprites.draw(self.screen)
        font = pygame.font.Font(None, 50)
        text = font.render('scores:' + str(SCORE), True, 'white')
        screen.blit(text, (10, 10))
        self.clock.tick(60)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        global SCORE, ENEMIES_COUNT

        fon = pygame.transform.scale(load_image('backgroundfonsettings.jpg'), (screen_width, screen_height))
        screen.blit(fon, (0, 0))

        restart_btn = SystemButton('', 225, 70)

        text = self.font.render('GAME OVER', True, 'WHITE')
        text_rect = text.get_rect(center=(800 / 2, 600 / 2))

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu_start()
            screen.blit(fon, (0, 0))

            if restart_btn.is_pressed():
                SCORE = 0
                ENEMIES_COUNT = 0
                self.new()
                self.main()
            restart_btn.draw(300, 400, 'RESTART', game_begin)

            self.screen.blit(text, text_rect)
            self.clock.tick(60)
            pygame.display.update()

    def game_vin(self):
        global SCORE, ENEMIES_COUNT

        fon = pygame.transform.scale(load_image('backgroundfonsettings.jpg'), (screen_width, screen_height))
        screen.blit(fon, (0, 0))

        vin_btn = SystemButton('', 225, 70)

        text = self.font.render('VICTORY', True, 'WHITE')
        text_rect = text.get_rect(center=(800 / 2, 600 / 2))

        cur.execute(
            f"""UPDATE scores set score = {SCORE}
                                           where player_id = (select id from player where name = '{NAME}')""")
        con.commit()

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                    self.running = False
            screen.blit(fon, (0, 0))

            if vin_btn.is_pressed():
                SCORE = 0
                ENEMIES_COUNT = 0
                menu_start()
            SCORE = 0
            vin_btn.draw(300, 400, 'MENU', menu_start)

            self.screen.blit(text, text_rect)
            self.clock.tick(60)

            self.clock.tick(60)
            pygame.display.update()


if __name__ == '__main__':
    menu_start()
