import math
import pygame
from pygame.locals import *
import random
import os

pygame.init()


# Colors

red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Sprites

pills = pygame.image.load('assets\images\pills.png')
bg = pygame.image.load('assets\images\papap.jpg')
water1shoot = pygame.image.load('assets\images\pwater.png')


walkRight = [pygame.image.load('assets\images\psurvivor.png'), pygame.image.load(
    'assets\images\psurvivorRun.png'), pygame.image.load('assets\images\psurvivorRun2.png'), pygame.image.load('assets\images\psurvivor.png'), pygame.image.load(
    'assets\images\psurvivorRun.png'), pygame.image.load('assets\images\psurvivorRun2.png'), pygame.image.load('assets\images\psurvivor.png'), pygame.image.load(
    'assets\images\psurvivorRun.png'), pygame.image.load('assets\images\psurvivorRun2.png')]
survivorStanding = pygame.image.load(
    'assets\images\psurvivorStanding.png')
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
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 30, True)
score = 0
items_spawn_time = [1000, 20, 30]
global_time = pygame.time.get_ticks()
dt = clock.tick()


class suriv(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [x + 20, end + 20]
        self.hitbox = [self.x, self.y, 50, 50]
        self.health = 1
        self.visible = True

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if self.vel > 0:
                screen.blit(surivMoving[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(surivMoving[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(
                screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 5, 30, 10))
            pygame.draw.rect(
                screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 5, 30 - (3 * (1 - self.health)), 10))
            self.hitbox = (self.x, self.y, 31, 57)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self, ):
        if self.health >= 0:
            self.health -= 1
        else:
            self.visible = False


class item(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.image = image

    def draw(self, screen):
        screen.blit(pills, (self.x, self.y))


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.isJumping = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = [self.x + 50, self.y + 80, 90, 150]
        self.health = 10
        self.isAlive = True

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
        pygame.draw.rect(
            screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 30, 100, 10))
        pygame.draw.rect(
            screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 30, 100 - (5 * (10 - self.health)), 10))
        self.hitbox = [self.x + 50, self.y + 80, 90, 150]

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


class projectile(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing
        self.hitbox = [self.x, self.y, 50, 50]

    def draw(self, screen):
        screen.blit(water1shoot, (self.x, self.y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def redrawWindow():
    survivor.draw(screen)
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    screen.blit(text, (390, 10))

    for suriv in weakSurivs:
        suriv.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()


survivor = player(40, 300, 64, 64)
weakSurivs = []
maxEnemies = 5
for enemy in range(maxEnemies):
    weakSurivs.append(suriv(random.randint(0, display_width), random.randint(
        100, 300), 64, 64, 800))

bullets = []
shootLoop = 0
run = True
bgX = 0
pill = item(100, 100, 50, 50)
global_time += dt

while run:
    pygame.time.delay(15)
    rel_x = bgX % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < display_width:
        screen.blit(bg, (rel_x, 0))
    bgX -= 1

    if len(weakSurivs) <= 3:
        pill.draw(screen)

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
            collision = isCollision(suriv.x, suriv.y, bullet.x, bullet.y)
            if collision:
                suriv.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                weakSurivs.pop(weakSurivs.index(suriv))

    for bullet in bullets:
        if bullet.x > display_width or bullet.x < 0:
            bullets.pop(bullets.index(bullet))
        else:
            bullet.x += bullet.vel

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if survivor.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 10:
            bullets.append(projectile(round(
                survivor.x + survivor.width // 2), round(survivor.y + survivor.height // 3), facing))
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
