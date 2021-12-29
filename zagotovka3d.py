import math

import pygame

pygame.init()
HEIGHT = 800
WIDTH = 1200
HALF_HEIGHT = HEIGHT // 2
HALF_WIDTH = WIDTH // 2
sc = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
TILE = 100 # сторорна клетки

# ray casting settings
FOV = math.pi / 3  # это область видимости которое мы сами задаем пусть это будет 180 / 3 = 60
HALF_FOV = FOV / 2
NUM_RAYS = 200  # количество лучей в диапазоне облатси видимости
MAX_DEPTH = 800  # растояние по прямой которое исходит из центра нашего расположения и задает максимальую длину видимости
DELTA_ANGLE = FOV / NUM_RAYS  # угол между лучами которые расположены в диапазоне области видимости
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV)) # расстояние от игрока до спроецируемого изображения
PROJ_COEFF = DIST * TILE
SCALE = WIDTH // NUM_RAYS  # масштабирующий коэфициент из-за того, что пайтон медленный при работе с количествами лучами равными шириине

player_pos = (HALF_WIDTH, HALF_HEIGHT)
player_angle = 0 # угол под которым смотрит наше направление
player_speed = 2

clock = pygame.time.Clock()

map = [
    'WWWWWWWWWWWW',
    'W......W...W',
    'W..WWW...W.W',
    'W....W..WW.W',
    'W..W....W..W',
    'W..W...WWW.W',
    'W....W.....W',
    'WWWWWWWWWWWW'
]

world_map = list()
for j, row in enumerate(map):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.append((i * TILE, j * TILE))


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.position = ()

    def pos(self):
        self.position = (self.x, self.y)
        return self.position

    def movement(self):
        cos_angle = math.cos(self.angle)
        sin_angle = math.sin(self.angle)
        self.mouse_control()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y += player_speed * sin_angle
            self.x += player_speed * cos_angle
        if keys[pygame.K_s]:
            self.y += -player_speed * sin_angle
            self.x += -player_speed * cos_angle
        if keys[pygame.K_a]:
            self.x += player_speed * sin_angle
            self.y += -player_speed * cos_angle
        if keys[pygame.K_d]:
            self.x += -player_speed * sin_angle
            self.y += player_speed * cos_angle
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
        if keys[pygame.K_ESCAPE]:
            exit()
        # print(self.x, self.y)
        # print(world_map)
        """нужно реализовать не прохождение через стены"""

    def mouse_control(self):
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * 0.006  # этот параметр можно менять, так как он отвечает за чувствительностью точнее за изменением угла


def ray_casting(sc, player_pos, player_angle):
    ox, oy = player_pos
    xm, ym = (ox // TILE) * TILE, (oy // TILE) * TILE  # находим пересечение с клтекой и его координаты (клетки)
    begin_ray_angle = player_angle - HALF_FOV # угол для первого луча
    for ray in range(NUM_RAYS):
        cos_a = math.cos(begin_ray_angle)
        sin_a = math.sin(begin_ray_angle)

        # для нахождения пересенчения с вертикалью у клетки
        if cos_a >= 0:
            x = xm + TILE
            dx = 1
        else:
            x = xm
            dx = -1
        for i in range(0, WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if (((x + dx) // TILE) * TILE, (y // TILE) * TILE) in world_map:
                break
            x += dx * TILE

        # для поиска пересечеия с горизонталью у клетки
        if sin_a >= 0:
            y = ym + TILE
            dy = 1
        else:
            y = ym
            dy = -1
        for i in range(0, HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if ((x // TILE) * TILE, ((y + dy) // TILE) * TILE) in world_map:
                break
            y += dy * TILE

        if depth_h < depth_v:
            depth = depth_h
        else:
            depth = depth_v
        # fix fish eye effect
        depth *= math.cos(player_angle - begin_ray_angle)

        proj_height = PROJ_COEFF / (depth + 0.000001)

        color = 255 / (1 + depth * depth * 0.0002)

        pygame.draw.rect(sc, (int(color), int(color), int(color)),
                         ((ray * SCALE, (HALF_HEIGHT - proj_height // 2)), (SCALE, proj_height)))
        begin_ray_angle += DELTA_ANGLE


def begin_game():
    player = Player()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                running = False
        player.movement()
        sc.fill('BLACK')
        pygame.draw.rect(sc, 'BLUE', (0, 0, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(sc, 'BROWN', (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
        position = player.pos()
        ray_casting(sc, position, player.angle)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    begin_game()
