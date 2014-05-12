#!/usr/bin/python

# python
import json
import random

# gtk
from gi.repository import Gtk

# pygame
import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEMOTION, VIDEORESIZE, ACTIVEEVENT

# app
import PlanetaryScreens
from PlanetaryScreens import Home, Play


class Planetary:

    def __init__(self):

        # running vars
        self.running = True # controls the exit of the game loop
        self.data = None  # check out init_data.json for the structure
        self.clock = pygame.time.Clock() # controls the frame rate
        self.forceAll = False # force an entire repaint of the screen on the next frame
        self.question = ""
        self.answer = ""


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

        # game screens
        self.homeScreen = Home()
        self.playScreen = Play()

        # set the initial screen
        self.currentScreen = self.playScreen


        # The main game loop.
        while self.running:
            
            # Pump GTK events
            while Gtk.events_pending():
                Gtk.main_iteration()

            # read the daily news
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                elif event.type == VIDEORESIZE or event.type == ACTIVEEVENT:
                    self.forceAll = True

                elif event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    name = self.currentScreen.pointCollide(pos)
                    print name

                elif event.type == MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    self.currentScreen.mousemove(pos)

            # switch for current screen
            if self.currentScreen == self.homeScreen:
                pass
            elif self.currentScreen == self.playScreen:
                pass
            
            if self.forceAll:
                print "force"

            # update the screen
            self.currentScreen.frame(self.forceAll)
            self.forceAll = False

            # keep at 30fps
            self.clock.tick(30)

        # End of game loop
        pygame.quit()


    # retrieves a question in play from the list
    def getQuestion(self):
        pass

    # retrieves a fact that was not in play from the list
    def getFact(self):
        pass


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
