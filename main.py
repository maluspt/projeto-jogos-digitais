import math
import pygame
from pygame.locals import *
import random
import os

menu_selecao = 3
os.environ['SDL_VIDEO_CETERED'] = '1'
pygame.init()
botao_enter = False

# Colors

red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Sprites

pills = pygame.image.load('assets\images\pills.png')
alcool = pygame.image.load('assets\images\palcool.png')
firstaid = pygame.image.load('assets\images\pfirstaid.png')
medicine = pygame.image.load('assets\images\medicine.png')

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
surivStanding = pygame.image.load('assets\images\corona1.png')
redSuriv1 = pygame.transform.scale(surivStanding, (50, 50))
surivStanding2 = pygame.image.load('assets\images\corona5.png')
greenSuriv1 = pygame.transform.scale(surivStanding2, (50, 50))
surivStanding3 = pygame.image.load('assets\images\corona8.png')
blueSuriv1 = pygame.transform.scale(surivStanding3, (50, 50))

# Sounds
audio_menu = pygame.mixer.Sound("assets/sounds/menu1.ogg")
audio_confirmar = pygame.mixer.Sound('assets/sounds/confirmation_002.ogg')
audio_jogo = pygame.mixer.Sound('assets/sounds/jogo.ogg')
shoot = pygame.mixer.Sound('assets/sounds/shoot.ogg')
boost = pygame.mixer.Sound('assets/sounds/boost.ogg')

# Screen
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 30, True)
main_font = pygame.font.SysFont("comicsans", 50)
lost_font = pygame.font.SysFont("comicsans", 60)


class Suriv(object):
    COLOR_MAP = {
        "red": redSuriv1,
        "green": greenSuriv1,
        "blue": blueSuriv1
    }

    def __init__(self, x, y, width, height, end, health, color):
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
        self.img = self.COLOR_MAP[color]

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        self.walkCount += 1
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.hitbox[0], self.hitbox[1] - 5, 30, 10))
        pygame.draw.rect(
            screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 5, 30 - (3 * (3 - self.health)), 10))
        self.hitbox = (self.x, self.y, 30, 30)

    def move(self, vel):
        self.x -= vel

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

    def get_width(self):
        return self.img.get_width()


class item(object):
    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img

    def draw(self, screen):
        screen.blit(self.img, (self.x + 200, self.y + 200))


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
        self.health = 20
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
            screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 30, 100 - ((20 - self.health)), 10))
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


def changeBackgroung(bg, bgX):
    rel_x = bgX % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < display_width:
        screen.blit(bg, (rel_x, 0))


pillItem = item(50, 50, 50, 50, pills)
alcoolItem = item(200, 50, 50, 50, alcool)
firstAidItem = item(300, 50, 50, 50, firstaid)


def main():
    bullets = []
    items = [pillItem, alcoolItem, firstAidItem]
    shootLoop = 0
    run = True
    level = 0
    bgX = 0
    lost = False
    FPS = 60
    lost_count = 0
    score = 0
    survivor = player(40, 300, 64, 64)
    enemies = []
    maxEnemies = 5
    enemy_vel = 2

    def redrawWindow():
        survivor.draw(screen)
        text = font.render("Score: " + str(score), 1, (0, 0, 0))
        screen.blit(text, (390, 10))

        for surivs in enemies:
            surivs.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        screen.blit(level_label, (display_width -
                                  level_label.get_width() - 10, 10))

        if lost:
            lost_label = lost_font.render("GAME OVER!", 1, (255, 255, 255))
            screen.blit(lost_label, (display_width/2 -
                                     lost_label.get_width()/2, 350))
        pygame.display.update()

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

        if len(enemies) == 0:
            level += 1
            maxEnemies += 5
            for i in range(maxEnemies):
                enemy = Suriv(random.randint(0, display_width),
                              random.randint(100, 300), 64, 64, 800, 1, random.choice(["red", "green", "blue"]))
                enemies.append(enemy)

        if level == 1:
            changeBackgroung(bgForest, bgX)
            bgX -= 1
        if level == 2:
            changeBackgroung(bgForest2, bgX)
            bgX -= 1
            pygame.time.delay(15)
        if level == 3:
            changeBackgroung(bgDesert, bgX)
            bgX -= 1
            pygame.time.delay(15)

        if score >= 3:
            items[0].draw(screen)
        if score >= 10:
            items[1].draw(screen)
        if score >= 20:
            items[2].draw(screen)

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
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
            shoot.play()
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

        for bullet in bullets:
            if bullet.x > display_width or bullet.x < 0:
                bullets.pop(bullets.index(bullet))
            else:
                bullet.x += bullet.vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            for bullet in bullets:
                if isCollision(enemy.x, enemy.y, bullet.x, bullet.y):
                    enemy.hit()
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
            if enemy.x + enemy.img.get_width() < 0:
                enemies.remove(enemy)
                survivor.hit()

        for item in items:
            if isCollision(item.x, item.y, survivor.x, survivor.y):
                items.remove(item)
                boost.play()
                print("a")

        if level == 3:
            if len(enemies) == 0:
                main_menu()


def eventos():
    global menu_selecao, botao_enter
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    menu_selecao += 1
                if event.key == K_UP:
                    menu_selecao -= 1
                if event.key == K_RETURN:
                    menu_selecao += 10

def selecao():

        global menu_selecao, botao_enter

        if menu_selecao == 3:
            screen.blit(bgForest, (0, 0))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            ranking = fonte.render("> Ranking <", True, (80, 80, 80))
            screen.blit(ranking, ((display_width / 2) - 50, (display_height / 2) + 44))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            sobre = fonte.render("Sobre", True, (80, 80, 80))
            screen.blit(sobre, ((display_width / 2) - 50, (display_height / 2) + 66))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            sair = fonte.render("Sair", True, (80, 80, 80))
            screen.blit(sair, ((display_width / 2) - 50, (display_height / 2) + 88))

        if menu_selecao == 4:
            screen.blit(bgForest, (0, 0))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            ranking = fonte.render("Ranking", True, (80, 80, 80))
            screen.blit(ranking, ((display_width / 2) - 50, (display_height / 2) + 44))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            sobre = fonte.render("> Sobre <", True, (80, 80, 80))
            screen.blit(sobre, ((display_width / 2) - 50, (display_height / 2) + 66))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            sair = fonte.render("Sair", True, (80, 80, 80))
            screen.blit(sair, ((display_width / 2) - 50, (display_height / 2) + 88))

        if menu_selecao == 5:
            screen.blit(bgForest, (0, 0))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            ranking = fonte.render("Ranking", True, (80, 80, 80))
            screen.blit(ranking, ((display_width / 2) - 50, (display_height / 2) + 44))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            sobre = fonte.render("Sobre", True, (80, 80, 80))
            screen.blit(sobre, ((display_width / 2) - 50, (display_height / 2) + 66))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            sair = fonte.render("> Sair <", True, (80, 80, 80))
            screen.blit(sair, ((display_width / 2) - 50, (display_height / 2) + 88))

        if menu_selecao == 6:
            menu_selecao = 5

        if menu_selecao == 0:
            menu_selecao = 1

        if menu_selecao == 14:
            menu_selecao = 400

        if menu_selecao == 400:
            screen.blit(bgForest, (0, 0))

            fonte = pygame.font.SysFont("comicsans", 20, False, False)
            fonte_render = fonte.render("---- Criado por: ---- ", True, (80, 80, 80))
            fonte_render1 = fonte.render("---- Ana Carolina Dias da Cunha - TIA: ----", True, (80, 80, 80))
            fonte_render2 = fonte.render("---- Maria Luiza - TIA: ----", True, (80, 80, 80))
            fonte_render3 = fonte.render("---- Stefan Jong Heun Oh - TIA: ----", True, (80, 80, 80))
            voltar_render = fonte.render("> Voltar <", True, (80, 80, 80))

            screen.blit(fonte_render, ((display_width / 2)-130, (display_height/2)))
            screen.blit(fonte_render1, ((display_width / 2) -130, (display_height / 2)+20))
            screen.blit(fonte_render2, ((display_width / 2) -130, (display_height / 2)+40))
            screen.blit(fonte_render3, ((display_width / 2) -130, (display_height / 2)+60))
            screen.blit(voltar_render, ((display_width / 2) -45, (display_height / 2)+100))

        if menu_selecao == 401:
            menu_selecao = 400

        if menu_selecao == 399:
            menu_selecao = 400

        if menu_selecao == 410:
            menu_selecao = 4

        if menu_selecao == 15:
            menu_selecao = 500

        if menu_selecao == 500:
            pygame.quit()
            exit()

while True:
    title_font = pygame.font.SysFont("comicsans", 30)
    audio_menu.play()
    print(botao_enter)
    print(menu_selecao)
    eventos()
    selecao()
    title_label = title_font.render(
        "Pressione o botao do mouse para jogar!", 1, (80, 80, 80))
    screen.blit(title_label, (display_width / 2 -
                              title_label.get_width() / 2, 250))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            audio_confirmar.play()
            audio_menu.stop()
            main()
pygame.quit()
