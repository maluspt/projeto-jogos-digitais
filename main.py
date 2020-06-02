import math
import pygame
from pygame.locals import *
import random

pygame.init()

# Colors

red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Sprites

pills = pygame.image.load('assets\images\pills.png')
bg = pygame.image.load('assets\images\papap.jpg')

walkRight = [pygame.image.load('assets\images\psurvivor.png'), pygame.image.load(
    'assets\images\psurvivorRun.png'), pygame.image.load('assets\images\psurvivorRun2.png'), pygame.image.load('assets\images\psurvivor.png'), pygame.image.load(
    'assets\images\psurvivorRun.png'), pygame.image.load('assets\images\psurvivorRun2.png'), pygame.image.load('assets\images\psurvivor.png'), pygame.image.load(
    'assets\images\psurvivorRun.png'), pygame.image.load('assets\images\psurvivorRun2.png')]
survivorStanding = pygame.image.load('assets\images\psurvivorStanding.png')
survivorJumping = pygame.image.load('assets\images\pjump.png')

surivMove = pygame.image.load('assets\images\corona2.png')
surivStanding = pygame.image.load('assets\images\corona1.png')
redSuriv1 = pygame.transform.scale(surivStanding, (50, 50))
redSuriv2 = pygame.transform.scale(surivMove, (50, 50))
surivMoving = [redSuriv1, redSuriv2, redSuriv1, redSuriv2,
               redSuriv1, redSuriv2, redSuriv1, redSuriv2, redSuriv1]
# Screen
display_width = 800
display_height = 600
bgX = 0
bgX2 = bg.get_width()
x = (display_width * 0.45)
y = (display_height * 0.8)
speed = 6
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()


class suriv(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = [self.x, self.y, 50, 50]

    def draw(self, screen):
        self.move()
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.vel < 0:
            screen.blit(surivMoving[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        print("hit")


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 1
        self.isJumping = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = [self.x + 50, self.y + 80, 90, 150]

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if (self.isJumping):
            screen.blit(survivorJumping, (self.x, self.y))
        elif not(self.standing):
            if self.left:
                screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(survivorStanding, (self.x, self.y))
            else:
                screen.blit(survivorStanding, (self.x, self.y))


class projectile(object):
    def __init__(self, x, y, r, color, facing):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.facing = facing
        self.vel = 5 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


def redrawWindow():
    screen.blit(bg, (bgX, 0))
    screen.blit(bg, (bgX2, 0))
    survivor.draw(screen)

    for suriv in weakSurivs:
        suriv.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()


survivor = player(40, 300, 64, 64)
weakSurivs = []
maxEnemies = 10
for enemy in range(maxEnemies):
    weakSurivs.append(suriv(random.randint(0, display_width), random.randint(
        0, display_height), 64, 64, 800))

bullets = []
shootLoop = 0
run = True

while run:
    pygame.time.delay(15)
    bgX -= 1
    bgX2 -= 1

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    for suriv in weakSurivs:
        if suriv.x < display_width and suriv.x > 0:
            suriv.x += suriv.vel

    for bullet in bullets:
        for suriv in weakSurivs:
            if bullet.y - bullet.r < suriv.hitbox[1] + suriv.hitbox[3] and bullet.y + bullet.r > suriv.hitbox[1]:
                if bullet.x + bullet.r > suriv.hitbox[0] and bullet.x - bullet.r < suriv.hitbox[0] + suriv.hitbox[2]:
                    suriv.hit()
                    bullets.pop(bullets.index(bullet))

    for bullet in bullets:
        if bullet.x < display_width and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if survivor.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 10:
            bullets.append(projectile(round(
                survivor.x + survivor.width * 2), round(survivor.y + survivor.height * 3), 6, blue, facing))
        shootLoop = 1
    if keys[pygame.K_LEFT] and survivor.x > survivor.vel:
        survivor.x -= survivor.vel
        survivor.left = True
        survivor.right = False
        survivor.standing = False
    elif keys[pygame.K_RIGHT] and survivor.x < display_width - survivor.width - survivor.vel:
        survivor.x += survivor.vel
        survivor.left = False
        survivor.right = True
        survivor.standing = False
    else:
        survivor.standing = True
        survivor.walkCount = 0
    if not(survivor.isJumping):
        if keys[pygame.K_UP] and survivor.y > survivor.vel:
            survivor.isJumping = True
            survivor.left = False
            survivor.right = False
            survivor.walkCount = 0
    else:
        if survivor.jumpCount >= -10:
            neg = 1
            if survivor.jumpCount < 0:
                neg = -1
            survivor.y -= (survivor.jumpCount ** 2) * 0.5 * neg
            survivor.jumpCount -= 1
        else:
            survivor.isJumping = False
            survivor.jumpCount = 10

    redrawWindow()


pygame.quit()
