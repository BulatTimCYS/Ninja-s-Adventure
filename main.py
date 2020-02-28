# import pygame
# from pygame import *
#
# scr = pygame.display.set_mode((1280, 720))
# pygame.display.set_caption("Ninja's Adventure")
#
#
# class Player(sprite.Sprite):
#     def __init__(self):
#         sprite.Sprite.__init__(self)
#         self.onGround = False
#         self.state = pygame.image.load('data/ninja.png')
#         self.run = pygame.image.load('data/ninja_run.png')
#         self.runleft = pygame.image.load('data/ninja_run_left.png')
#         self.xvel = 0
#         self.yvel = 0
#         self.startX = 0
#         self.startY = 0
#         self.rect = Rect(0, 0, 80, 80)
#         self.image = 0
#
#     def set_hero(self, x, y):
#         self.xvel = 0
#         self.startX = x
#         self.startY = y
#         self.rect.move(x, y)
#         self.image = 0
#
#     def update(self, left, right, up, down):
#         if left:
#             self.xvel = -7
#             self.image = 2
#
#         if right:
#             self.xvel = 7
#             self.image = 1
#
#         if self.onGround:
#             self.yvel = -10
#
#         if not self.onGround:
#             self.yvel += 10
#
#         if not (left or right):
#             self.xvel = 0
#             self.image = 0
#         self.onGround = False
#         self.rect.y += self.yvel
#         self.rect.x += self.xvel
#
#     def draw(self, screen):
#         if self.image == 0:
#             screen.blit(self.state, (self.rect.x, self.rect.y))
#         elif self.image == 1:
#             screen.blit(self.run, (self.rect.x, self.rect.y))
#         elif self.image == 2:
#             screen.blit(self.runleft, (self.rect.x, self.rect.y))
#
#
# class Enemy:
#     def __init__(self):
#         self.d = []
#         self.image = pygame.image.load('data/enemy.png')
#
#     def add_guard(self, x, y, alive=True, reverse=False):
#         self.d.append([x, y, alive, reverse])
#
#     def clear(self):
#         self.d = []
#
#     def draw(self, screen):
#         for i in range(len(self.d)):
#             screen.blit(self.image, (self.d[i][0], self.d[i][1]))
#
#
# class Lamp:
#     def __init__(self):
#         self.image = pygame.image.load('data/lamp.png')
#         self.d = []
#
#     def add_lamp(self, x, y):
#         self.d.append((x, y))
#
#     def clear(self):
#         self.d = []
#
#     def draw(self, screen):
#         for i in range(len(self.d)):
#             screen.blit(self.image, self.d[i])
#
#
# class Platform(sprite.Sprite):
#     def __init__(self, x, y):
#         sprite.Sprite.__init__(self)
#         self.image = Surface((80, 80))
#         self.downwall = pygame.image.load('data/down.png')
#         self.rect = Rect(x, y, 80, 80)
#
#
# class Map:
#     def __init__(self):
#         self.stairs = pygame.image.load('data/stairs.png')
#         self.g = []
#         self.map = 1
#         self.lastmap = 0
#         self.get_map()
#
#     def get_map(self):
#         f = open("data/map")
#         self.d = []
#         i = 0
#         l = f.readlines()
#         while len(l) > 9:
#             self.d.append(l[len(l) - 9:])
#             l = l[:len(l) - 9]
#         f.close()
#
#     def map_change(self):
#         if self.map == self.lastmap:
#             return
#         x = y = 0
#         m = 0
#         for row in self.d[m]:
#             for col in row:
#                 if col == "#":
#                     pf = Platform(x, y)
#                     entities.add(pf)
#                     platforms.append(pf)
#                 elif col == "/":
#                     scr.blit(self.stairs, (x, y))
#                 elif col == "X":
#                     hero.set_hero(x, y)
#                 elif col == "I":
#                     enemy.add_guard(x, y)
#                 elif col == "^":
#                     lamp.add_lamp(x, y)
#                 x += 80
#             y += 80
#             x = 0
#
#
# bg = pygame.image.load('data/background.png')
# running = True
# hero = Player()
# enemy = Enemy()
# lamp = Lamp()
# entities = pygame.sprite.Group()    # Все объекты
# platforms = []      # то, во что мы будем врезаться или опираться
# entities.add(hero)
# map = Map()
# left = right = down = up = False
# timer = pygame.time.Clock()
# while running:
#     timer.tick(60)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == KEYDOWN and event.key == K_LEFT:
#             left = True
#         if event.type == KEYDOWN and event.key == K_RIGHT:
#             right = True
#         if event.type == KEYDOWN and event.key == K_UP:
#             up = True
#         if event.type == KEYUP and event.key == K_UP:
#             up = False
#         if event.type == KEYUP and event.key == K_RIGHT:
#             right = False
#         if event.type == KEYUP and event.key == K_LEFT:
#             left = False
#     scr.blit(bg, bg.get_rect())
#     map.map_change()
#     # scr.fill(pygame.Color("#000000"))
#     lamp.draw(scr)
#     enemy.draw(scr)
#     hero.update(left, right, up, down)
#     entities.draw(scr)
#     pygame.display.flip()

import pygame
from pygame import *

# Объявляем переменные
WIN_WIDTH = 1280  # Ширина создаваемого окна
WIN_HEIGHT = 720  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((80, 80))
        self.image = image.load("data/platform.png")
        self.rect = Rect(x, y, 80, 80)


class ClearPlatform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((80, 80))
        self.image.fill(Color("#888888"))
        self.image.set_colorkey(Color("#888888"))
        self.rect = Rect(x, y, 80, 80)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = Surface((67, 80))
        self.rect = Rect(x, y, 67, 80)  # прямоугольный объект
        self.last = True

    def update(self, left, right, up, platforms):

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -11
            self.image = image.load("data/ninja_right.png")

        if left:
            self.xvel = -10  # Лево = x- n
            self.last = False
            if up:  # для прыжка влево есть отдельная анимация
                self.image = image.load("data/ninja_run_left.png")
            else:
                self.image = image.load("data/ninja_run_left.png")

        if right:
            self.xvel = 10  # Право = x + n
            self.last = True
            if up:
                self.image = image.load("data/ninja_run_right.png")
            else:
                self.image = image.load("data/ninja_run_right.png")

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                if self.last:
                    self.image = image.load("data/ninja_right.png")
                else:
                    self.image = image.load("data/ninja_left.png")

        if not self.onGround:
            self.yvel += 0.4

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает


def main():
    global hero
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Ninja's Adventure")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg = image.load("data/background.png")
    left = right = False
    up = False

    entities = pygame.sprite.Group()
    platforms = []

    level = []
    f = open("data/map")
    for i in f.readlines():
        level.append(i.replace("\n", ""))
    f.close()

    timer = pygame.time.Clock()
    x = y = 0
    for row in level:
        for col in row:
            if col == "#":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "X":
                hero = Player(x, y)
                entities.add(hero)
            if col == "0":
                pf = ClearPlatform(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += 80
        y += 80
        x = 0

    total_level_width = len(level[0]) * 80
    total_level_height = len(level) * 80

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:
        timer.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit("QUIT")
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False

        screen.blit(bg, (0, 0))

        camera.update(hero)
        hero.update(left, right, up, platforms)
        for event in entities:
            screen.blit(event.image, camera.apply(event))

        pygame.display.update()


if __name__ == "__main__":
    main()
