#!/usr/bin/env python
#
# Maze generator example using pygame/SDL
#
# Adapted from:
#    https://github.com/rm-hull/maze/blob/master/src/maze/generator.clj
#    https://github.com/rm-hull/pcd8544/blob/master/examples/maze.py

import pygame
import time
import st7735fb
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
                pygame.draw.lines(screen, borderColor, False, map(lambda (a,b): (scale(a),scale(b)), line))

        pygame.draw.rect(screen, borderColor, (0,0,scale(self.width)+1,scale(self.height)+1), 1)
        pygame.display.update()

def demo(iterations):
    borderColor = (255,255,255)
    fb = st7735fb.Framebuffer()

    for loop in range(iterations):
        for scale in [2,3,4,3]:
            sz = map(lambda z: z/scale-1, fb.size)
            Maze(sz).render(fb.screen, borderColor, lambda z: z * scale)

if __name__ == "__main__":
    demo(5)

