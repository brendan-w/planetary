#!/usr/bin/python


import json
from gi.repository import Gtk

import pygame
from pygame.locals import QUIT

from PlanetaryScreens import Home, Play


class Planetary:

    def __init__(self):

        # running vars
        self.running = True
        self.data = None  # check out init_data.json for the structure
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.get_surface()

        # game screens
        self.homeScreen = Home(pygame.display)
        self.playScreen = Play(pygame.display)

        # set the initial screen
        self.currentScreen = self.homeScreen


    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        f = open(file_path, 'r')
        self.data = json.load(f)
        f.close()

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        f = open(file_path, 'w')
        json.dump(self.data, f)
        f.close()

    # The main game loop.
    def run(self):
        
        # The main game loop.
        while self.running:
            
            # Pump GTK events
            while Gtk.events_pending():
                Gtk.main_iteration()

            # read the daily news
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

            # switch for current screen
            if self.currentScreen == self.homeScreen:
                pass
            elif self.currentScreen == self.playScreen:
                pass

            # update the window surface
            self.currentScreen.frame()

            # keep at 30fps
            self.clock.tick(30)

        # End of game loop
        pygame.quit()
        


# This function is called when the game is run directly from the command line:
# ./Planetary.py
def main():
    pygame.init()
    pygame.display.set_mode((1200, 900), pygame.RESIZABLE)
    game = Planetary()
    game.read_file("init_data.json")
    game.run()

if __name__ == '__main__':
    main()
