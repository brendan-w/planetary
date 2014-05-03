'''
System for handling pygame screens efficiently

Screens are handed dictionaries containing the settings for the screen.
These settings are filtered for changes, and only the changed graphics
are drawn to the screen. Switching screens forces all elements to be redrawn.
'''

import pygame


lastScreen = None


'''
Base class for screens
'''
class Screen(object):

	def __init__(self, display):
		self.display = display
		self.window = display.get_surface()
		self.updateRegions = []
		self.params = {}
		self.oldParams = {}

	def isNewScreen(self):
		global lastScreen
		return (lastScreen != self)

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
		global lastScreen
		lastScreen = self
		self.display.update(self.updateRegions)
		self.updateRegions = []
		self.oldParams = self.params.copy()



'''
Class that draws the home screen
'''
class Home(Screen):
	def __init__(self, display):
		super(Home, self).__init__(display)

		# default parameter list
		self.params = {
			"background": False,
		}

		self.oldParams = self.params.copy()

	def frame(self):
		changedParams = super(Home, self).getChanges()

		for key in changedParams:
			self.updateRegions.append(self.draw(key));

		super(Home, self).frame()

	# object drawing routines. Returns Rect of area modified
	def draw(self, key):
		if key == "background":
			print "draw"
			if self.params[key]:
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

