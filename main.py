import pygame
from pygame import *

WIN_WIDTH = 1280
WIN_HEIGHT = 720
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(DISPLAY)
pygame.init()
mouse.set_visible(False)


class Wall(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((80, 80))
        self.image = image.load("data/wall.png")
        self.rect = Rect(x, y, 80, 80)


class Lamp(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((80, 80))
        self.image = image.load("data/lamp.png")
        self.rect = Rect(x, y, 80, 80)


class SmallPlatform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((80, 3))
        self.x, self.y = x, y - 2
        self.image = image.load("data/floor.png")
        self.rect = Rect(x, y, 80, 1)


def initWalls(smps, walls, height):
    for i in smps:
        for j in range(i.y, height, 80):
            w = Wall(i.x, j)
            walls.add(w)


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


class Colona(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((80, 80))
        self.image = image.load("data/platform.png")
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
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.image = Surface((67, 79))
        self.rect = Rect(x - 6, y, 45, 79)
        self.last = True

    def update(self, left, right, up, platforms):

        if up:
            if self.onGround:
                self.yvel = -8

        if left:
            self.xvel = -10
            self.last = False
            if up:
                self.image = image.load("data/ninja_run_left.png")
            else:
                self.image = image.load("data/ninja_run_left.png")

        if right:
            self.xvel = 10
            self.last = True
            if up:
                self.image = image.load("data/ninja_run_right.png")
            else:
                self.image = image.load("data/ninja_run_right.png")

        if not (left or right):
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

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0


def start_screen():
    intro_text = ["Ninja's Adventure", "",
                  "Управление",
                  "W - Прыгнуть. A, D - Влево и вправо",
                  "Esc, чтобы выйти"]
    screen.fill(Color("#777722"))
    font = pygame.font.Font(None, 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 500
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key in [K_F4, KMOD_ALT]) or (event.type == pygame.QUIT) or (
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                raise SystemExit("QUIT")
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(60)


def stop_screen():
    mixer.music.stop()
    intro_text = ["Конец игры", "",
                  "Esc, чтобы выйти из игры",
                  "R, чтобы сделать перезапуск игры"]
    screen.fill(Color("#772222"))
    font = pygame.font.Font(None, 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 500
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key in [K_F4, KMOD_ALT]) or (event.type == pygame.QUIT) or (
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                raise SystemExit("QUIT")
            elif event.type == pygame.KEYDOWN and event.key == K_r:
                main()
        pygame.display.flip()
        clock.tick(60)


def main():
    global hero
    pygame.display.set_caption("Ninja's Adventure")
    bg = image.load("data/background.png")
    left = right = False
    up = down = False

    entities = pygame.sprite.Group()
    platforms = []
    smallplatforms = []
    walls = pygame.sprite.Group()

    level = []
    f = open("data/map")
    for i in f.readlines():
        level.append(i.replace("\n", ""))
    f.close()

    timer = pygame.time.Clock()
    x = y = 0
    flag_walls = False
    for row in level:
        for col in row:
            if col == "X":
                hero = Player(x, y)
                entities.add(hero)
            if flag_walls:
                wall = Wall(x, y)
                entities.add(wall)
            if col == "[":
                flag_walls = True
                colona = Colona(x, y)
                platforms.append(colona)
                entities.add(colona)
            if col == "]":
                flag_walls = False
                colona = Colona(x, y)
                platforms.append(colona)
                entities.add(colona)
            if col == "#":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "0":
                pf = ClearPlatform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "^":
                lamp = Lamp(x, y)
                entities.add(lamp)
            if col == "_":
                smp = SmallPlatform(x, y)
                smallplatforms.append(smp)
                platforms.append(smp)
                entities.add(smp)
            x += 80
        y += 80
        x = 0

    total_level_width = len(level[0]) * 80
    total_level_height = len(level) * 80

    camera = Camera(camera_configure, total_level_width, total_level_height)
    start_screen()
    pygame.mixer.music.load('data\music.mp3')
    pygame.mixer.music.play()
    while 1:
        timer.tick(60)
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key in [K_F4, KMOD_ALT]:
                pygame.quit()
                raise SystemExit("QUIT")
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                stop_screen()
            if (event.type == KEYDOWN) and (event.key == K_UP or event.key == K_w):
                up = True
            if (event.type == KEYDOWN) and (event.key == K_LEFT or event.key == K_a):
                left = True
            if (event.type == KEYDOWN) and (event.key == K_RIGHT or event.key == K_d):
                right = True
            # if event.type == KEYDOWN and event.key == K_DOWN:
            #     down = True
            #
            # if event.type == KEYUP and event.key == K_DOWN:
            #     down = False
            if (event.type == KEYUP) and (event.key == K_UP or event.key == K_w):
                up = False
            if (event.type == KEYUP) and (event.key == K_LEFT or event.key == K_a):
                left = False
            if (event.type == KEYUP) and (event.key == K_RIGHT or event.key == K_d):
                right = False

        screen.blit(bg, (0, 0))

        camera.update(hero)
        for wall in walls:
            screen.blit(wall.image, camera.apply(wall))
        hero.update(left, right, up, platforms)
        for event in entities:
            screen.blit(event.image, camera.apply(event))

        pygame.display.update()


if __name__ == "__main__":
    main()
