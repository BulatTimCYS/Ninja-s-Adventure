import pygame
from pygame import *

WIN_WIDTH = 1280
WIN_HEIGHT = 720
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(DISPLAY)
pygame.init()
mouse.set_visible(False)


class Door(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("data/door.png")
        self.rect = Rect(x + 37, y, 6, 80)


class Stairs(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("data/stairs.png")
        self.rect = Rect(x, y, 80, 80)


class Roof(sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        sprite.Sprite.__init__(self)
        if not inverted:
            self.image = image.load("data/roof.png")
        else:
            self.image = image.load("data/roof_inverted.png")
        self.rect = Rect(x, y, 80, 80)


class Wall(sprite.Sprite):
    def __init__(self, x, y, door=False):
        sprite.Sprite.__init__(self)
        if not door:
            self.image = image.load("data/wall.png")
            self.rect = Rect(x, y, 80, 80)
        else:
            self.image = image.load("data/doorwall.png")
            self.rect = Rect(x + 37, y, 43, 80)


class Lamp(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("data/lamp.png")
        self.rect = Rect(x, y, 80, 1)


class SmallPlatform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
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

    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h)


class Enemy(sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        sprite.Sprite.__init__(self)
        self.inverted = inverted
        if not inverted:
            self.image = image.load("data/enemy.png")
        else:
            self.image = image.load("data/inverted_enemy.png")
        self.rect = Rect(x, y, 80, 79)
        self.death = False


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.onStairs = False
        self.image = Surface((67, 79))
        self.rect = Rect(x - 6, y, 45, 79)
        self.last = True
        self.lastAction = False

    def update(self, left, right, up, down, action, platforms, stairs, enemies, targets):
        if up:
            if self.onGround or self.onStairs:
                self.yvel = -10

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
            self.yvel += 0.6

        self.onGround = False
        if sprite.spritecollide(self, stairs, False):
            self.onStairs = True
            if up:
                self.yvel = -7
            elif down:
                self.yvel = 7
            else:
                self.yvel = 0
        else:
            self.onStairs = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, enemies, action, targets)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, enemies, action, targets)

    def collide(self, xvel, yvel, platforms, enemies, action, targets):
        for p in platforms:
            if sprite.collide_rect(self, p):

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

        for e in enemies:
            if not e.death:
                if e.inverted:
                    if e.rect.x + 20 <= self.rect.x <= e.rect.x + 120 and (
                            e.rect.y <= self.rect.y + 79 <= e.rect.y or e.rect.y <= self.rect.y <= e.rect.y + 79) and action:
                        e.death = True
                        e.image = image.load("data/inverted_dead_enemy.png")
                    if (e.rect.x - 320 < self.rect.x < e.rect.x + 20 or e.rect.x < self.rect.x < e.rect.x + 20) and (
                            e.rect.y < self.rect.y + 60 < e.rect.y + 79 or e.rect.y < self.rect.y < e.rect.y + 60) and not e.death:
                        stop_screen()
                else:
                    if e.rect.x - 100 <= self.rect.x + 80 <= e.rect.x + 60 and (
                            e.rect.y <= self.rect.y + 79 <= e.rect.y or e.rect.y <= self.rect.y <= e.rect.y + 79) and action:
                        e.death = True
                        e.image = image.load("data/dead_enemy.png")
                    if (e.rect.x + 60 < self.rect.x < e.rect.x + 380 or e.rect.x + 60 < self.rect.x + 80 < e.rect.x + 80) and (
                            e.rect.y < self.rect.y + 60 < e.rect.y + 79 or e.rect.y < self.rect.y < e.rect.y + 60) and not e.death:
                        stop_screen()
        for t in targets:
            if not t.death:
                if (t.rect.x - 50 < self.rect.x + 80 < t.rect.x + 80 or t.rect.x + 130 > self.rect.x > t.rect.x) and (
                        t.rect.y < self.rect.y + 60 < t.rect.y + 79 or t.rect.y < self.rect.y < t.rect.y + 60) and action:
                    t.death = True
                    t.image = image.load("data/dead_target.png")
        targets_alive(targets)


def targets_alive(targets):
    dcount = 0
    for t in targets:
        if t.death:
            dcount += 1
    if dcount == len(targets):
        win_screen()


class Target(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("data/target.png")
        self.rect = Rect(x, y, 80, 80)
        self.death = False


def start_screen():
    intro_text = ["Ninja's Adventure", "",
                  "Твоя задача - помочь ниндзе",
                  "в последнем задании - вытащить из плена мальчика", "", ""
                  "Управление",
                  "W - Прыгнуть. A, D - Влево и вправо",
                  "S - Вниз по лестнице, E или пробел - действие",
                  "Также можно использовать стрелочки",
                  "Esc, чтобы выйти"]
    screen.fill(Color("#227777"))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
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
                return
        pygame.display.flip()
        clock.tick(60)


def pause_screen():
    mixer.music.pause()
    intro_text = ["Пауза", "",
                  "Esc, чтобы вернуться",
                  "Alt+F4, чтобы выйти из игры",
                  "R, чтобы сделать перезапуск игры"]
    screen.fill(Color("#777722"))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                global left, right, up, down, action
                left = right = up = down = action = False
                mixer.music.unpause()
                return
            elif event.type == pygame.KEYDOWN and event.key == K_r:
                main()
            elif (event.type == KEYDOWN and event.key in [K_F4, KMOD_ALT]) or (event.type == pygame.QUIT):
                pygame.quit()
                raise SystemExit("quit")
        pygame.display.flip()
        clock.tick(60)


def stop_screen():
    mixer.music.stop()
    intro_text = ["Ты не справился с заданием...", "",
                  "Esc, чтобы выйти из игры",
                  "R, чтобы сделать перезапуск игры"]
    screen.fill(Color("#772222"))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
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


def win_screen():
    mixer.music.stop()
    intro_text = ["Вы завершили последенее задание ниндзи", "",
                  "Esc, чтобы выйти из игры",
                  "R, чтобы сделать перезапуск игры"]
    screen.fill(Color("#579232"))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
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
    global hero, left, up, right, down, action
    pygame.display.set_caption("Ninja's Adventure")
    bg = image.load("data/background.png")
    left = right = False
    up = down = False
    action = False

    entities = pygame.sprite.Group()
    platforms = []
    smallplatforms = []
    enemies = sprite.Group()
    doors = sprite.Group()
    stairs = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    targets = pygame.sprite.Group()

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
            if flag_walls:
                wall = Wall(x, y)
                entities.add(wall)
            if col == "-":
                flag_walls = True
                doorwall = Wall(x, y, door=True)
                entities.add(doorwall)
                door = Door(x, y)
                doors.add(door)
                entities.add(door)
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
            if col == "/":
                roof = Roof(x, y)
                platforms.append(roof)
                entities.add(roof)
            if col == "\\":
                roof = Roof(x, y, inverted=True)
                platforms.append(roof)
                entities.add(roof)
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
                smallplatforms.append(lamp)
                platforms.append(lamp)
                entities.add(lamp)
            if col == "_":
                smp = SmallPlatform(x, y)
                smallplatforms.append(smp)
                platforms.append(smp)
                entities.add(smp)
            if col == "|":
                stair = Stairs(x, y)
                stairs.add(stair)
                entities.add(stair)
            if col == ">":
                enemy = Enemy(x, y)
                enemies.add(enemy)
            if col == "<":
                enemy = Enemy(x, y, inverted=True)
                enemies.add(enemy)
            if col == "x":
                target = Target(x, y)
                targets.add(target)
            x += 80
        y += 80
        x = 0

    total_level_width = len(level[0]) * 80
    total_level_height = len(level) * 80

    camera = Camera(camera_configure, total_level_width, total_level_height)
    start_screen()
    pygame.mixer.music.load('data\music.mp3')
    mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
    while 1:
        timer.tick(60)
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key in [K_F4, KMOD_ALT]:
                pygame.quit()
                raise SystemExit("QUIT")
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pause_screen()
            if (event.type == KEYDOWN) and (event.key == K_UP or event.key == K_w):
                up = True
            if (event.type == KEYDOWN) and (event.key == K_LEFT or event.key == K_a):
                left = True
            if (event.type == KEYDOWN) and (event.key == K_RIGHT or event.key == K_d):
                right = True
            if event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_s):
                down = True
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_e):
                action = True

            if event.type == KEYUP and (event.key == K_SPACE or event.key == K_e):
                action = False
            if event.type == KEYUP and (event.key == K_DOWN or event.key == K_s):
                down = False
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
        hero.update(left, right, up, down, action, platforms, stairs, enemies, targets)
        for item in entities:
            screen.blit(item.image, camera.apply(item))
        screen.blit(hero.image, camera.apply(hero))
        for e in enemies:
            screen.blit(e.image, camera.apply(e))
        for d in doors:
            screen.blit(d.image, camera.apply(d))
        for t in targets:
            screen.blit(t.image, camera.apply(t))
        pygame.display.update()


if __name__ == "__main__":
    main()
