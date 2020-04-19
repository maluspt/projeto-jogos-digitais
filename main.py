import math
import pygame
from pygame.locals import *
from random import randint 

pygame.init()

red = (255, 0, 0)
blue = (0, 0, 255)
white = (255,255,255)
display_width = 800
display_height = 1000
pills = pygame.image.load('assets\images\pills.png')
bg = pygame.image.load('assets\images\papap.png')
bgX = 0
bgX2 = bg.get_width()
run = True
speed = 4

screen = pygame.display.set_mode((display_width, display_height))


class Monster:
    def __init__(self , x, y, r):
        self.x = x
        self.y = y
        self.r = r

class Survivor:
    def show(self, x, y):
        screen.blit(pills, (x, y))

monsters = []
survivor = Survivor()
x =  (display_width * 0.45)
y = (display_height * 0.8)

screen.fill(white)
survivor.show(x, y)

def redrawWindow():
    screen.blit(bg, (bgX, 0))  # draws our first bg image
    screen.blit(bg, (bgX2, 0))  # draws the seconf bg image
    pygame.display.update()  


while run:
    redrawWindow()
    bgX -= 0.1  # Move both background images back
    bgX2 -= 0.1

    if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX = bg.get_width()
    
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            quit()
    pygame.display.update()
