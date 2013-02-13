#!/usr/bin/env python

import pygame
import st7735fb
import time

fb = st7735fb.Framebuffer()
array = pygame.PixelArray(fb.screen)

for (x,y) in [(x,y) for x in xrange(fb.width) \
                    for y in xrange(fb.height)]:

    color = (fb.width-x>>3) << 16 \
                  | (x>>2) << 8  \
                  | (y>>2) << 0

    array[x][y] = color

pygame.display.update()
time.sleep(5)
