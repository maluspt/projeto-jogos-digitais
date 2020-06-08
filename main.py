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
bgForest = pygame.image.load('assets\images\pforest.jpg')
bgForest2 = pygame.image.load('assets\images\pforest2.png')
bgDesert = pygame.image.load('assets\images\pdesert.png')
water1shoot = pygame.image.load('assets\images\pwater.png')


walkRight = [pygame.image.load('assets\images\psurvivor.png'), pygame.image.load(
    'assets\images\psurvivorRun.png'), pygame.image.load('assets\images\psurvivorRun2.png'), pygame.image.load('assets\images\psurvivor.png'), pygame.image.load(
    'assets\images\psurvivorRun.png'), pygame.image.load('assets\images\psurvivorRun2.png'), pygame.image.load('assets\images\psurvivor.png'), pygame.image.load(
    'assets\images\psurvivorRun.png'), pygame.image.load('assets\images\psurvivorRun2.png')]

walkLeft = [pygame.image.load('assets\images\psurvivorleft.png'), pygame.image.load(
    'assets\images\psurvivorRunleft.png'), pygame.image.load('assets\images\psurvivorRun2left.png'), pygame.image.load('assets\images\psurvivorleft.png'), pygame.image.load(
    'assets\images\psurvivorRunleft.png'), pygame.image.load('assets\images\psurvivorRun2left.png'), pygame.image.load('assets\images\psurvivorleft.png'), pygame.image.load(
    'assets\images\psurvivorRunleft.png'), pygame.image.load('assets\images\psurvivorRun2left.png')]
survivorStanding = pygame.image.load(
    'assets\images\psurvivorStanding.png')
survivorJumping = pygame.image.load('assets\images\pjump.png')
survivorDown = pygame.image.load('assets\images\psurvivordown.png')
survivorStandingLeft = pygame.image.load(
    'assets\images\psurvivorStandingleft.png')


# Weak surivs
surivMove = pygame.image.load('assets\images\corona2.png')
surivStanding = pygame.image.load('assets\images\corona1.png')
redSuriv1 = pygame.transform.scale(surivStanding, (50, 50))
redSuriv2 = pygame.transform.scale(surivMove, (50, 50))
surivMoving = [redSuriv1, redSuriv2, redSuriv1, redSuriv2,
               redSuriv1, redSuriv2, redSuriv1, redSuriv2, redSuriv1]

# Medium surivs

surivMove2 = pygame.image.load('assets\images\corona4.png')
surivStanding2 = pygame.image.load('assets\images\corona5.png')
surivStanding22 = pygame.image.load('assets\images\corona6.png')
greenSuriv1 = pygame.transform.scale(surivStanding2, (50, 50))
greenSuriv2 = pygame.transform.scale(surivMove2, (50, 50))
greenSuriv3 = pygame.transform.scale(surivStanding22, (50, 50))
surivMoving2 = [greenSuriv1, greenSuriv2, greenSuriv3, greenSuriv1,
                greenSuriv2, greenSuriv3, greenSuriv1, greenSuriv2, greenSuriv3]

# Strong surivs

surivMove3 = pygame.image.load('assets\images\corona7.png')
surivStanding3 = pygame.image.load('assets\images\corona8.png')
surivStanding33 = pygame.image.load('assets\images\corona9.png')
blueSuriv1 = pygame.transform.scale(surivStanding3, (50, 50))
blueSuriv2 = pygame.transform.scale(surivMove3, (50, 50))
blueSuriv3 = pygame.transform.scale(surivStanding33, (50, 50))
surivMoving3 = [blueSuriv1, blueSuriv2, blueSuriv3, blueSuriv1,
                blueSuriv2, blueSuriv3, blueSuriv1, blueSuriv2, blueSuriv3]


# Screen
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 30, True)
score = 0
main_font = pygame.font.SysFont("comicsans", 50)
lost_font = pygame.font.SysFont("comicsans", 60)


class suriv(object):
    def __init__(self, x, y, width, height, end, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [x + 30, end + 30]
        self.hitbox = [self.x, self.y, 50, 50]
        self.health = health
        self.visible = True

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if level == 1:
                screen.blit(
                    surivMoving[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            if level == 2:
                screen.blit(
                    surivMoving2[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            if level == 3:
                screen.blit(
                    surivMoving3[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(
                screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 5, 30, 10))
            pygame.draw.rect(
                screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 5, 30 - (3 * (3 - self.health)), 10))
            self.hitbox = (self.x, self.y, 30, 30)

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

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


class item(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.image = image

    def draw(self, screen):
        screen.blit(pills, (self.x + 200, self.y + 200))


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
                screen.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(survivorStanding, (self.x, self.y))
            else:
                screen.blit(survivorStandingLeft, (self.x, self.y))
        pygame.draw.rect(
            screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 30, 100, 10))
        pygame.draw.rect(
            screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 30, 100 - (10 * (10 - self.health)), 10))
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
        self.hitbox = [self.x, self.y, 10, 10]

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

    for suriv in enemies:
        suriv.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
    screen.blit(level_label, (display_width -
                              level_label.get_width() - 10, 10))

    if lost:
        lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
        screen.blit(lost_label, (display_width/2 -
                                 lost_label.get_width()/2, 350))
    pygame.display.update()


def changeBackgroung(bg, bgX):
    rel_x = bgX % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < display_width:
        screen.blit(bg, (rel_x, 0))


survivor = player(40, 300, 64, 64)
enemies = []
maxEnemies = 6

for enemy in range(maxEnemies):
    enemies.append(suriv(random.randint(0, display_width), random.randint(
        100, 300), 64, 64, 800, 1))

for enemy in range(maxEnemies):
    enemies.append(suriv(random.randint(0, display_width), random.randint(
        100, 300), 64, 64, 800, 2))

for enemy in range(maxEnemies):
    enemies.append(suriv(random.randint(0, display_width), random.randint(
        100, 300), 64, 64, 800, 3))


bullets = []
shootLoop = 0
run = True
level = 1
bgX = 0
lost = False
FPS = 60
lost_count = 0
pill = item(random.randint(0, display_width + 50), random.randint(
    0, display_height + 50), 50, 50)

while run:
    clock.tick(FPS)
    pygame.time.delay(15)
    redrawWindow()

    if survivor.health <= 0:
        lost = True
        lost_count += 1

    if lost:
        if lost_count > FPS * 3:
            run = False
        else:
            continue

    if level == 1:
        changeBackgroung(bgForest, bgX)
        bgX -= 1
    if score >= 8 and score < 15:
        level = 2
        changeBackgroung(bgForest2, bgX)
        bgX -= 1
        pygame.time.delay(15)
        for suriv in enemies:
            suriv.draw(screen)
    if score >= 15:
        level = 3
        changeBackgroung(bgDesert, bgX)
        bgX -= 1
        pygame.time.delay(15)
        for suriv in enemies:
            suriv.draw(screen)

    if score >= 3:
        pill.draw(screen)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

# First lvl

    for suriv in enemies:
        collision = isCollision(suriv.x, suriv.y, survivor.x, survivor.y)
        if collision:
            survivor.hit()

    for suriv in enemies:
        if suriv.x < display_width and suriv.x > 0:
            suriv.x += suriv.vel

    for bullet in bullets:
        for suriv in enemies:
            collision = isCollision(suriv.x, suriv.y, bullet.x, bullet.y)
            if collision:
                suriv.hit()
                bullets.pop(bullets.index(bullet))
                enemies.pop(enemies.index(suriv))
                score += 1

# Second lvl

    for suriv in enemies:
        if suriv.x < display_width and suriv.x > 0:
            suriv.x += suriv.vel

    for bullet in bullets:
        for suriv in enemies:
            collision = isCollision(suriv.x, suriv.y, bullet.x, bullet.y)
            if collision:
                suriv.hit()
                bullets.pop(bullets.index(bullet))
                enemies.pop(enemies.index(suriv))
                score += 1


# Last lvl

    for suriv in enemies:
        if suriv.x < display_width and suriv.x > 0:
            suriv.x += suriv.vel

    for bullet in bullets:
        for suriv in enemies:
            collision = isCollision(suriv.x, suriv.y, bullet.x, bullet.y)
            if collision:
                suriv.hit()
                bullets.pop(bullets.index(bullet))
                enemies.pop(enemies.index(suriv))
                score += 1

    for bullet in bullets:
        if bullet.x > display_width or bullet.x < 0:
            bullets.pop(bullets.index(bullet))
        else:
            bullet.x += bullet.vel

    # Game keys

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if survivor.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 3:
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


pygame.quit()
