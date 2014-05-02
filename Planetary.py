#!/usr/bin/python


import json

import pygame
from pygame.locals import QUIT

from gi.repository import Gtk



class Planetary:

    def __init__(self):
        self.running = True
        self.data = None  # check out init_data.json for the structure
        self.window =pygame.display.get_surface()
        self.clock = pygame.time.Clock()


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
                    pygame.quit()
                    self.running = False

            # list for the update regions
            update_regions = list()

            # game logic

            # update the window surface

            # keep at 30fps
            self.clock.tick(30)
        


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
