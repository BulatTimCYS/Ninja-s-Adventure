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


class Map:
    def __int__(self):
        pass


def map_change():
    d = ["                ",
         "                ",
         "                ",
         "                ",
         "                ",
         "                ",
         "    /___________",
         "_X_/__I_^_______",
         "################"]
    x = y = 0  # координаты
    for row in d:  # вся строка
        for col in row:  # каждый символ
            if col == "#":
                scr.blit(pygame.image.load('data/down.png'), (x, y))
            elif col == "/":
                scr.blit(pygame.image.load('data/stairs.png'), (x, y))
            elif col == "X":
                scr.blit(pygame.image.load('data/ninja.png'), (x, y))
            elif col == "I":
                scr.blit(pygame.image.load('data/enemy.png'), (x, y))
            elif col == "^":
                scr.blit(pygame.image.load('data/flashlight.png'), (x, y))
            x += 80  # блоки платформы ставятся на ширине блоков
        y += 80  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля



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
    map_change()
    pygame.display.flip()

# TODO:
# Сделать движок
# Спрайты
# Меню
# Презентация
