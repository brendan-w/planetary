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
from PlanetaryConstants import *
import PlanetaryScreens
from PlanetaryScreens import Home, Play


class Planetary:

    def __init__(self):

        # running vars
        self.running = True # controls the exit of the game loop
        self.clock = pygame.time.Clock() # controls the frame rate
        self.forceAll = False # force an entire repaint of the screen on the next frame
        self.clicked = None # the ID of the object that was clicked

        # question data
        self.data = None  # check out init_data.json for the structure
        self.liveQuestions = None
        self.waitQuestions = None

        # game logic
        self.question = None # the question the user is currently answering
        self.lastQuestion = None # prevents the same question from being asked twice in a row
        self.answer = None # tuple (win/loose, planet clicked)
        self.gameWait = 0 # frame counter for timers (counts UP from zero)
        self.gameState = 0 # what stage in the round
        '''
        Game States:
            0 = display new question
            1 = wait for answer (planet click)
            2 = display result (win/fail)
            3 = display correct answer(s)
            4 = display new fact
            5 = wait for confirmation (button click)
        '''

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

        # load and build graphics
        PlanetaryScreens.load()
        self.homeScreen = Home()
        self.playScreen = Play()

        # set the initial screen
        self.screen = self.playScreen


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
                    self.clicked = self.screen.click(pos)
                
                elif event.type == MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    self.screen.mousemove(pos)

            ''' 
            switch for current screen
            '''
            if self.screen == self.homeScreen:
                pass

            elif self.screen == self.playScreen:
                '''
                switch for game state
                '''
                if self.gameState == 0: #============================================
                    # choose a new question
                    self.getQuestion()
                    # display the question
                    self.screen.setText(self.question["question"])
                    self.screen.setAllColor(GLOW_WHITE)
                    self.screen.mouseOverEnabled = True
                    self.advance()

                elif self.gameState == 1: #============================================
                    if self.clicked in PLANETS:
                        win = self.testAnswer(self.clicked)
                        self.answer = (win, self.clicked) # store the users answer so it can be displayed later
                        
                        # display the result
                        if win:
                            color = GLOW_GREEN
                            self.screen.setText(WIN_TEXT)
                        else:
                            color = GLOW_RED
                            self.screen.setText(LOSE_TEXT)

                        self.screen.startPulse(self.clicked, color)
                        self.screen.mouseOverEnabled = False
                        self.screen.hideText()
                        self.advance()

                elif self.gameState == 2: #============================================
                    # waiting stage (clicked planet is currently pulsing)
                    self.frameTimer(37)
                
                elif self.gameState == 3: #============================================
                    self.screen.stopPulse(self.answer[1])
                    if self.answer[0]:
                        # if they were right, do a flashy thing
                        self.screen.startRandomPulse(GLOW_GREEN)
                    else:
                        # if they were wrong, highlight pulse the correct planets
                        for planet in self.question["answers"]:
                            self.screen.startPulse(planet, GLOW_YELLOW)

                    self.advance()
                
                elif self.gameState == 4: #============================================
                    # waiting stage (correct planet/happy flash is being displayed)
                    self.frameTimer(40)
                
                elif self.gameState == 5: #============================================
                    self.screen.stopAllPulse()
                    self.screen.setText(NEXT_FACT_TEXT)
                    self.advance()

                elif self.gameState == 6: #============================================
                    # rest while user reads the "next fact" text
                    self.frameTimer(30)

                elif self.gameState == 7: #============================================
                    # fade out the "next fact" text
                    self.screen.hideText()
                    self.advance()

                elif self.gameState == 8: #============================================
                    # wait while text fades out
                    self.frameTimer(30)

                elif self.gameState == 9: #============================================
                    # choose the next fact
                    fact = self.getFact(self.answer[1])
                    # display the fact and its planets
                    self.screen.setText(fact["fact"])
                    for planet in fact["answers"]:
                        self.screen.startPulse(planet, GLOW_WHITE)

                    self.advance()

                elif self.gameState == 10: #============================================
                    # wait for confirmation from the user before user
                    if self.clicked == NEXT_BUTTON:
                        self.screen.stopAllPulse()
                        self.screen.hideText()
                        self.loop() # that's it! go back to gameState = 0




            # update the screen
            self.screen.frame(self.forceAll)

            # reset frame variables
            self.forceAll = False
            self.clicked = None

            # keep at 30fps
            self.clock.tick(30)

        # End of game loop
        pygame.quit()

    # End of run function


    # advances the game state once the given timer has expired
    def frameTimer(self, value):
        if self.gameWait >= value:
            self.advance()
        else:
            self.gameWait += 1

    # advances the game state
    def advance(self):
        self.gameWait = 0
        self.gameState += 1

    # send the game state back to the beginning
    def loop(self):
        self.gameWait = 0
        self.gameState = 0

    # chooses a new question for the user, and loads it into self.question
    def getQuestion(self, prevAnswer=None):
        self.checkData()

        self.lastQuestion = self.question

        while self.question == self.lastQuestion:
            self.question = random.choice(self.liveQuestions)


    # search for a new fact (with question) linearly with an fact about the planet clicked
    # returns the new question on success, false if no questions left  <--  you beat the game
    def getFact(self, prevAnswer=None):
        self.checkData()

        if len(self.waitQuestions) > 0:
            newQuestion = None
            for question in self.waitQuestions:
                if self.testAnswer(prevAnswer, question):
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


    # are you a winner? or are you a FAILURE
    def testAnswer(self, answer, question=None):
        if question == None:
            question = self.question

        return answer in question["answers"]


    # in case sugar never called readFile, load the default game state
    def checkData(self):
        if self.data == None:
            self.read_file("init_data.json")


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
