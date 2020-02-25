import pygame

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


class Lamp:
    def __init__(self, x, y):
        self.coordinates = (x, y)


class Block:
    def __init__(self, x, y):
        self.coordinates = (x, y)


scr.blit(pygame.image.load('data/background.png'), pygame.image.load('data/background.png').get_rect())
running = True
hero = Hero(0, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.ARROWRIGHT:
        #     hero.get_click(event.pos)
    scr.blit(pygame.image.load('data/background.png'), pygame.image.load('data/background.png').get_rect())
    pygame.display.flip()

# TODO:
# Сделать движок
# Спрайты
# Меню
# Презентация
