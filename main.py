import math
import pygame
from pygame.locals import *
from random import randint

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

surivMove = [pygame.image.load('assets\images\corona1.png'), pygame.image.load('assets\images\corona2.png'), pygame.image.load('assets\images\corona3.png'), pygame.image.load('assets\images\corona4.png'), pygame.image.load(
    'assets\images\corona5.png'), pygame.image.load('assets\images\corona6.png'), pygame.image.load('assets\images\corona7.png'), pygame.image.load('assets\images\corona8.png'), pygame.image.load('assets\images\corona9.png')]
surivStanding = pygame.image.load('assets\images\corona1.png')
test = pygame.transform.scale(surivStanding, (50, 50))
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
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        screen.blit(test, (self.x, self.y))


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

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.left:
            screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            screen.blit(survivorStanding, (self.x, self.y))


def redrawWindow():
    screen.blit(bg, (bgX, 0))
    screen.blit(bg, (bgX2, 0))
    weakSuriv.draw(screen)
    survivor.draw(screen)
    pygame.display.update()


survivor = player(40, 300, 64, 64)
weakSuriv = suriv(400, 100, 50, 50)
run = True

while run:
    pygame.time.delay(15)
    bgX -= 1
    bgX2 -= 1

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and survivor.x > survivor.vel:
        survivor.x -= survivor.vel
        survivor.left = True
        survivor.right = False
    elif keys[pygame.K_RIGHT] and survivor.x < display_width - survivor.width - survivor.vel:
        survivor.x += survivor.vel
        survivor.left = False
        survivor.right = True
    else:
        survivor.right = False
        survivor.left = False
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
