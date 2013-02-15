#! /usr/bin/env python

import pygame
import st7735fb

y = 0
dir = 1
running = 1
barheight = 124
fb = st7735fb.Framebuffer()

barcolor = []
for i in range(1, 63):
    barcolor.append((0, 0, i*4))
for i in range(1, 63):
    barcolor.append((0, 0, 255 - i*4))

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    fb.screen.fill((0, 0, 0))
    for i in range(0, barheight):
        pygame.draw.line(fb.screen, barcolor[i], (0, y+i), (fb.width, y+i))

    y += dir
    if y + barheight > fb.height or y < 0:
        dir *= -1

    pygame.display.flip()
