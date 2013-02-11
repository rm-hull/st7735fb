#!/usr/bin/env python
#
# Maze generator example using pygame/SDL
#
# Adapted from:
#    https://github.com/rm-hull/maze/blob/master/src/maze/generator.clj
#    https://github.com/rm-hull/pcd8544/blob/master/examples/maze.py

import os
import sys
import pygame
import time
from random import randrange

NORTH=1
WEST=2

class Maze:

    def __init__(self, size):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.size = self.width * self.height
        self.generate()

    def offset(self, coords):
        """ Converts [x,y] co-ords into an offset in the maze data """
        return ((coords[1] % self.height) * self.width) + (coords[0] % self.width)

    def coords(self, offset):
        """ Converts offset to [x,y] co-ords """
        return (offset % self.width, offset / self.width)

    def neighbours(self, pos):
        neighbours = []

        if pos > self.width:
            neighbours.append(pos - self.width)

        if pos % self.width > 0:
            neighbours.append(pos - 1)

        if pos % self.width < self.width - 1:
            neighbours.append(pos + 1)

        if pos + self.width < self.size:
            neighbours.append(pos + self.width)

        return neighbours

    def is_wall_between(self, p1, p2):
        """ Checks to see if there is a wall between two (adjacent) points
            in the maze. The return value will indicate true if there is a
            wall else false. If the points aren't adjacent, false is
            returned. """
        if p1 > p2:
            return self.is_wall_between(p2, p1)

        if p2 - p1 == self.width:
            return self.data[p2] & NORTH != 0

        if p2 - p1 == 1:
            return self.data[p2] & WEST != 0

        return false;

    def knockdown_wall(self, p1, p2):
        """ Knocks down the wall between the two given points in the maze.
            Assumes that they are adjacent, otherwise it doesn't make any
            sense (and wont actually make any difference anyway) """
        if p1 > p2:
            return self.knockdown_wall(p2, p1)
        if p2 - p1 == self.width:
            self.data[p2] &= WEST

        if p2 - p1 == 1:
            self.data[p2] &= NORTH

    def generate(self):
        self.data = [ NORTH | WEST ] * self.size
        visited = { 0: True }
        stack = [0]
        not_visited = lambda x: not visited.get(x, False)

        while len(stack) > 0:
            curr = stack[-1]
            n = filter(not_visited, self.neighbours(curr))
            sz = len(n)
            if sz == 0:
                stack.pop()
            else:
                np = n[randrange(sz)]
                self.knockdown_wall(curr, np)
                visited[np] = True
                if sz == 1:
                    stack.pop()
                stack.append(np)

    def render(self, screen, borderColor=(255,255,255), scale=lambda a: a):

        screen.fill((0, 0, 0))
        for i in xrange(self.size):
            line = []
            p1 = self.coords(i)

            if self.data[i] & NORTH > 0:
                p2 = (p1[0]+1, p1[1])
                line.append(p2)
                line.append(p1)

            if self.data[i] & WEST > 0:
                p3 = (p1[0], p1[1]+1)
                line.append(p1)
                line.append(p3)

            if len(line) > 0:
                pygame.draw.lines(screen, borderColor, False, map(scale, line))

        pygame.draw.rect(screen, borderColor, (0,0) + scale((self.width,self.height)), 1)
        pygame.display.update()


class Demo:
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
                os.putenv('SDL_FBDEV', '/dev/fb1')
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % self.size
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

def demo(iterations):
    borderColor = (255,255,255)
    d = Demo()

    for loop in range(iterations):
        for scale in [2,3,4,3]:
            sz = map(lambda z: z/scale-1, d.size)
            Maze(sz).render(d.screen, borderColor, lambda (a,b): (a * scale, b * scale))


if __name__ == "__main__":
    demo(5)

