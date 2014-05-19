#!/usr/bin/python

'''
Main pygame file. Handles game logic and high-level UI management
'''

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
        self.clock = pygame.time.Clock() # controls the frame rate
        self.forceAll = False # force an entire repaint of the screen on the next frame
        self.data = None  # check out init_data.json for the structure
        self.liveQuestions = None
        self.waitQuestions = None

        self.currentQuestion = None
        self.lastQuestion = None

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        f = open(file_path, 'r')
        self.data = json.load(f)
        f.close()

        self.liveQuestions = self.data["live"]
        self.waitQuestions = self.data["wait"]


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

                elif event.type == MOUSEBUTTONUP and (event.button == 1 or event.button == 3):
                    pos = pygame.mouse.get_pos()
                    name = self.currentScreen.click(pos)
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


    # chooses a new question for the user, and loads it into self.currentQuestion
    def newQuestion(self, prevAnswer=None):
        self.checkData()
        
        self.lastQuestion = self.currentQuestion

        while self.currentQuestion == self.lastQuestion:
            self.currentQuestion = random.choice(self.liveQuestions)


    # search for a new fact (with question) linearly with an fact about the planet clicked
    # returns the new question on success, false if no questions left  <--  you beat the game
    def getFact(self, prevAnswer=None):
        self.checkData()

        if len(self.waitQuestions) > 0:

            newQuestion = None

            for question in self.waitQuestions:
                if testAnswer(prevAnswer):
                    newQuestion = question
                    break;

            # none left with this answer, choose at random
            if newQuestion == None:
                newQuestion = random.choice(self.waitQuestions)

            self.liveQuestions.append(newQuestion)
            self.waitQuestions.remove(newQuestion)
            return newQuestion
        else:
            return False


    def testAnswer(self, answer, question):
        if answer in question.answers:
            return True
        else:
            return False


    # in case sugar never called readFile, load the default game state
    def checkData(self):
        if self.data == None:
            self.readFile("init_data.json")


# This function is called when the game is run directly from the command line:
# ./Planetary.py
def main():
    pygame.init()
    pygame.display.set_mode((1200, 900), pygame.RESIZABLE)
    game = Planetary()
    #game.read_file("init_data.json")
    game.run()

if __name__ == '__main__':
    main()
