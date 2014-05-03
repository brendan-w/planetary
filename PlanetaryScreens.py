'''
System for handling STATIC pygame screens efficiently

Each screen object has a dict of settings called "params" that is modified by the game.
When frame() is called on a screen, it filters this dict for changes, and only
draws the changed graphics. Switching screens forces all elements to be redrawn.
'''


import pygame


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
		self.params = {}
		self.oldParams = {}

	def isNewScreen(self):
		global oldScreen
		return (oldScreen != self)

	def getChanges(self):
		if self.isNewScreen():
			return self.params
		else:
			changedParams = {}
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
	def __init__(self, display):
		super(Home, self).__init__(display)

		# load graphics for this screen
		self.graphics = {
			"a" : "<pygame load call>"
		}

		# default parameter list
		self.params = {
			"background": False,
		}

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
		elif key == "question":
			pass






'''
Class that draws the play screen
'''
class Play(Screen):
	def __init__(self, display):
		super(Play, self).__init__(display)

