#!/usr/bin/env python

# Snake game
#
# Make sure:
#   1. the 'st7735fb_map' module is loaded
#   2. the python-cwiid package is install

import pygame, sys, time, random
from pygame.locals import *
import st7735fb
import cwiid

fb = st7735fb.Framebuffer()
fpsClock = pygame.time.Clock()
playSurface = fb.screen

redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
blueColor = pygame.Color(0,0,255)
blackColor = pygame.Color(0,0,0)
whiteColor = pygame.Color(255,255,255)
greyColor = pygame.Color(150,150,150)

snakePosition = [9,9]
snakeSegments = [[9,9],[6,9],[3,9]]
raspberryPosition = [30,30]
raspberrySpawned = 1
direction = 'right'
changeDirection = direction
score = 0

def text(msg, font_size, color, posn):
    surf = pygame.font.Font('freesansbold.ttf', font_size).render(msg, True, color)
    rect = surf.get_rect()
    rect.midtop = posn
    playSurface.blit(surf, rect)
    pygame.display.flip();

def image(image_path, posn):
    surf = pygame.image.load(image_path)
    rect = surf.get_rect()
    rect.midtop = posn
    playSurface.blit(surf, rect)
    pygame.display.flip();

def start():
    text('Raspberry Snake', 12, blueColor, (64,2))
    image('images/rasp.png', (64,14))
    text('Press 1 + 2 on the Wiimote', 9, whiteColor, (64,150))

def gameOver():
    text('Game Over', 18, greyColor, (64,80))
    rumble()
    time.sleep(4)
    pygame.quit()
    sys.exit()

def displayScore(score):
    text('score: ' + str(score), 10, greenColor, (64,1))

def rumble():
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0

start()
time.sleep(1)

# Connect to the Wii Remote. If it times out
# then quit.
try:
  wii = cwiid.Wiimote()
except RuntimeError:
  print "Error opening wiimote connection"
  quit()

wii.rpt_mode = cwiid.RPT_BTN
rumble()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                changeDirection = 'right'
            if event.key == K_LEFT:
                changeDirection = 'left'
            if event.key == K_UP:
                changeDirection = 'up'
            if event.key == K_DOWN:
                changeDirection = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    buttons = wii.state['buttons']
    if (buttons & cwiid.BTN_RIGHT):
        changeDirection = 'right'
    if (buttons & cwiid.BTN_LEFT):
        changeDirection = 'left'
    if (buttons & cwiid.BTN_UP):
        changeDirection = 'up'
    if (buttons & cwiid.BTN_DOWN):
        changeDirection = 'down'

    if changeDirection == 'right' and not direction == 'left':
        direction = changeDirection
    if changeDirection == 'left' and not direction == 'right':
        direction = changeDirection
    if changeDirection == 'up' and not direction == 'down':
        direction = changeDirection
    if changeDirection == 'down' and not direction == 'up':
        direction = changeDirection

    if direction == 'right':
        snakePosition[0] += 3
    if direction == 'left':
        snakePosition[0] -= 3
    if direction == 'up':
        snakePosition[1] -= 3
    if direction == 'down':
        snakePosition[1] += 3

    snakeSegments.insert(0,list(snakePosition))

    if snakePosition[0] == raspberryPosition[0]    and snakePosition[1] == raspberryPosition[1]:
        raspberrySpawned = 0
        score += 1
    else:
        snakeSegments.pop()

    if raspberrySpawned == 0:
        x = random.randrange(1,42)
        y = random.randrange(1,53)
        raspberryPosition = [int(x)*3,int(y)*3]
    raspberrySpawned = 1

    playSurface.fill(blackColor)
    displayScore(score)
    for position in snakeSegments:
        pygame.draw.rect(playSurface,whiteColor,Rect(position[0],position[1],3,3))
        pygame.draw.rect(playSurface,redColor,Rect(raspberryPosition[0],raspberryPosition[1],3,3))
    pygame.display.flip()

    if snakePosition[0] >= 128 or snakePosition[0] < 0:
        gameOver()
    if snakePosition[1] >= 160 or snakePosition[1] < 0:
        gameOver()
    for snakeBody in snakeSegments[1:]:
        if snakePosition[0] == snakeBody[0] and snakePosition[1] == snakeBody[1]:
            gameOver()

    fpsClock.tick(20)
