#!/usr/bin/env python

import os
import sys
import pygame

class Framebuffer:
    def __init__(self, device='/dev/fb1'):
        "Iniitializes a new pygame screen using the framebuffer"
        os.system("modprobe st7735fb_map")
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
                os.putenv('SDL_FBDEV', device)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.size = (self.width, self.height)

        print "Framebuffer size: %d x %d" % self.size
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        pygame.font.init()
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

