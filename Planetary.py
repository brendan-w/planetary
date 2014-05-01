#!/usr/bin/python


import pygame
from gi.repository import Gtk


class Planetary:
    def __init__(self):
        pass

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    # The main game loop.
    def run(self):
        pass


# This function is called when the game is run directly from the command line:
# ./Planetary.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = Planetary()
    game.run()

if __name__ == '__main__':
    main()
