'''
System for handling STATIC pygame screens efficiently

Each screen object has a dict of settings called "params" that is modified by the game.
When frame() is called on a screen, it filters this dict for changes, and only
draws the changed graphics. Switching screens forces all elements to be redrawn.
'''


import pygame
from collections import OrderedDict


oldScreen = None


'''
Base class for screens
Handles parameter changes and update regions
'''
class Screen(object):

	def __init__(self):
		self.display = pygame.display
		self.window = pygame.display.get_surface()
		self.updateRegions = []
		self.params = OrderedDict()
		self.oldParams = OrderedDict()

	def isNewScreen(self):
		global oldScreen
		return (oldScreen != self)

	def getChanges(self):
		if self.isNewScreen():
			return self.params
		else:
			changedParams = OrderedDict()
			for key in self.params:
				if self.params[key] != self.oldParams[key]:
					changedParams[key] = self.params[key]
			return changedParams

	# show the changes, increment the param dictionaries
	def frame(self):
		global oldScreen
		oldScreen = self
		self.display.update(self.updateRegions)
		self.updateRegions = []
		self.oldParams = self.params.copy()





'''
Class that draws the home screen
'''
class Home(Screen):
	def __init__(self):
		super(Home, self).__init__()

		# load graphics for this screen
		self.graphics = {
			"test" : pygame.image.load("assets/python_test_600x600.png").convert()
		}

		# default parameter list
		self.params = OrderedDict([
			("background", False),
			("test", True),
		])

		# init the old parameters list
		self.oldParams = self.params.copy()


	def frame(self):
		changedParams = super(Home, self).getChanges()

		for key in changedParams:
			rect = self.draw(key, self.params[key])
			self.updateRegions.append(rect);

		super(Home, self).frame()

	# object drawing routines. Returns Rect of area modified
	def draw(self, key, value):
		if key == "background":
			if value:
				return pygame.Rect(0,0,0,0)
			else:
				return self.window.fill(pygame.Color(255,255,255))
		elif key == "test":
			if value:
				return self.window.blit(self.graphics["test"], (0,0))
			else:
				return pygame.Rect(0,0,0,0)






'''
Class that draws the play screen
'''
class Play(Screen):
	def __init__(self):
		super(Play, self).__init__()

