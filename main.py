import pygame
from pygame import *

scr = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Ninja's Adventure")


class Player(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.state = pygame.image.load('data/ninja.png')
        self.run = pygame.image.load('data/ninja_run.png')
        self.runleft = pygame.image.load('data/ninja_run_left.png')
        self.xvel = 0
        self.startX = 0
        self.startY = 0
        self.rect = Rect(0, 0, 80, 80)
        self.image = 0

    def set_hero(self, x, y):
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.rect.move(x, y)
        self.image = 0

    def update(self, left, right, down):
        if left:
            self.xvel = -7
            self.image = 2

        if right:
            self.xvel = 7
            self.image = 1

        if down:
            self.xvel = 0
            self.image = 3

        if not (left or right):
            self.xvel = 0
            self.image = 0

        self.rect.x += self.xvel

    def draw(self, screen):
        if self.image == 0:
            screen.blit(self.state, (self.rect.x, self.rect.y))
        elif self.image == 1:
            screen.blit(self.run, (self.rect.x, self.rect.y))
        elif self.image == 2:
            screen.blit(self.runleft, (self.rect.x, self.rect.y))


class Enemy:
    def __init__(self):
        self.d = []
        self.image = pygame.image.load('data/enemy.png')

    def add_guard(self, x, y, alive=True, reverse=False):
        self.d.append([x, y, alive, reverse])

    def clear(self):
        self.d = []

    def draw(self, screen):
        for i in range(len(self.d)):
            screen.blit(self.image, (self.d[i][0], self.d[i][1]))


class Lamp:
    def __init__(self):
        self.image = pygame.image.load('data/lamp.png')
        self.d = []

    def add_lamp(self, x, y):
        self.d.append((x, y))

    def clear(self):
        self.d = []

    def draw(self, screen):
        for i in range(len(self.d)):
            screen.blit(self.image, self.d[i])


class Map:
    def __init__(self):
        self.num = 1
        self.lastnum = 0
        self.downwall = pygame.image.load('data/down.png')
        self.stairs = pygame.image.load('data/stairs.png')
        self.g = []
        self.get_map()

    def get_map(self):
        f = open("data/map")
        self.d = []
        i = 0
        l = f.readlines()
        while len(l) > 9:
            self.d.append(l[len(l) - 9:])
            l = l[:len(l) - 9]
        f.close()
        print(self.d)

    def map_change(self):
        x = y = 0
        m = 0
        for row in self.d[m]:
            for col in row:
                if col == "#":
                    scr.blit(self.downwall, (x, y))
                elif col == "/":
                    scr.blit(self.stairs, (x, y))
                elif col == "X":
                    hero.set_hero(x, y)
                elif col == "I":
                    enemy.add_guard(x, y)
                elif col == "^":
                    lamp.add_lamp(x, y)
                x += 80
            y += 80
            x = 0


bg = pygame.image.load('data/background.png')
running = True
hero = Player()
enemy = Enemy()
lamp = Lamp()
map = Map()
left = right = down = False
timer = pygame.time.Clock()
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
    lamp.draw(scr)
    enemy.draw(scr)
    hero.update(left, right, False)
    hero.draw(scr)
    pygame.display.flip()
