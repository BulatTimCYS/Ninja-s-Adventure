import pygame
from pygame import *

scr = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Ninja's Adventure")


# def render(self):
#     global scr
#     for i in range(len(self.board)):
#         for j in range(len(self.board[i])):
#             if self.board[i][j]:
#                 pygame.draw.rect(scr, pygame.Color("white"),
#                                  (self.left + j * self.cell_size,
#                                   self.top + i * self.cell_size, self.cell_size, self.cell_size))
#             else:
#                 pygame.draw.rect(scr, pygame.Color("white"),
#                                  (self.left + j * self.cell_size,
#                                   self.top + i * self.cell_size, self.cell_size, self.cell_size), 1)


class Hero:
    def __init__(self, x, y, alive=True, dark=False):
        self.coordinates = (x, y)
        self.alive = alive
        self.dark = dark

    # def get_key(self, key):
    #     if key ==


# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.xvel = 0  # скорость перемещения. 0 - стоять на месте
#         self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
#         self.startY = y
#         self.image = pygame.Surface((80, 80))
#         self.image.fill(pygame.Color("#FFFFFF"))
#         self.rect = pygame.Rect(x, y, 80, 80)  # прямоугольный объект
#
#     def update(self, event):
#         left = right = False
#         if left:
#             self.xvel = -5  # Лево = x- n
#
#         if right:
#             self.xvel = 5  # Право = x + n
#
#         if not (left or right):  # стоим, когда нет указаний идти
#             self.xvel = 0
#
#         self.rect.x += self.xvel  # переносим свои положение на xvel
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
#             left = True
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
#             right = True
#
#         if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
#             right = False
#         if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
#             left = False
#
#     def draw(self, screen):  # Выводим себя на экран
#         screen.blit(self.image, (self.rect.x, self.rect.y))
class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.rect = Rect(x, y, 80, 80)  # прямоугольный объект
        self.image = 0
        self.state = pygame.image.load('data/ninja.png')
        self.run = pygame.image.load('data/ninja_run.png')
        self.runleft = pygame.image.load('data/ninja_run_left.png')

    def update(self, left, right):
        if left:
            self.xvel = -7  # Лево = x- n
            self.image = 2

        if right:
            self.xvel = 7  # Право = x + n
            self.image = 1

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            self.image = 0

        self.rect.x += self.xvel  # переносим свои положение на xvel

    def draw(self, screen):  # Выводим себя на экран
        if self.image == 0:
            screen.blit(self.state, (self.rect.x, self.rect.y))
        elif self.image == 1:
            screen.blit(self.run, (self.rect.x, self.rect.y))
        elif self.image == 2:
            screen.blit(self.runleft, (self.rect.x, self.rect.y))


class Enemy:
    def __init__(self, x, y, rad=10, radz=1, alive=True):
        self.coordinates = (x, y)
        self.vision = rad
        if radz == 1:
            self.vnavigate = "left"
        elif radz == 2:
            self.vnavigate = "up"
        elif radz == 3:
            self.vnavigate = "right"
        elif radz == 4:
            self.vnavigate = "down"
        else:
            self.vnavigate = "not"
        self.alive = alive
        self.image = pygame.image.load('data/enemy.png')

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect())


class Lamp:
    def __init__(self, x, y):
        self.image = pygame.image.load('data/flashlight.png')
        self.x = x
        self.y = y
    # scr.blit(, (x, y))


class Map:
    def __init__(self):
        self.d = []
        self.num = 1
        self.lastnum = 0
        self.downwall = pygame.image.load('data/down.png')
        self.stairs = pygame.image.load('data/stairs.png')
        self.g = []
        self.map_change()

    def get_map(self, k):
        self.d.clear()
        f = open("data/" + str(k) + "_map")
        for number, line in enumerate(f):
            self.d.append(line.rstrip())
        f.close()

    def map_change(self):
        if self.num != self.lastnum:
            self.lastnum = self.num
            self.get_map(self.num)
        x = y = 0
        for row in self.d:
            for col in row:
                if col == "#":
                    scr.blit(self.downwall, (x, y))
                elif col == "/":
                    scr.blit(self.stairs, (x, y))
                elif col == "X":
                    global herox, heroy
                    herox = x
                    heroy = y
                elif col == "I":
                    pass
                elif col == "^":
                    pass
                x += 80
            y += 80
            x = 0


bg = pygame.image.load('data/background.png')
running = True
herox, heroy = 0, 0
map = Map()
left = right = False  # по умолчанию — стоим
timer = pygame.time.Clock()
hero = Player(herox, heroy)
while running:
    timer.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_LEFT:
            left = True
        if event.type == KEYDOWN and event.key == K_RIGHT:
            right = True

        if event.type == KEYUP and event.key == K_RIGHT:
            right = False
        if event.type == KEYUP and event.key == K_LEFT:
            left = False
    scr.blit(bg, bg.get_rect())
    map.map_change()
    # scr.fill(pygame.Color("#000000"))
    hero.update(left, right)  # передвижение
    hero.draw(scr)  # отображение
    pygame.display.flip()

# TODO:
# Сделать движок
# Спрайты
# Меню
# Презентация
