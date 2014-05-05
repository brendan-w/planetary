'''
System for handling STATIC pygame screens efficiently

Each screen object has a dict of settings called "params" that is modified by the game.
When frame() is called on a screen, it filters this dict for changes, and only
draws the changed graphics. Switching screens forces all elements to be redrawn.
'''


import pygame
from collections import OrderedDict

from PlanetarySprites import Planet

# used for determining screen switches
oldScreen = None


'''
Asset handler
Call loadAssets AFTER pygame has initialized
'''
assets = {}
sprites = {}

def load():
	global assets
	global sprites

	assets = {
		"test" : pygame.image.load("assets/python_test_600x600.png").convert_alpha()
	}

	sprites = {
		"mercury" : Planet((50, 50), "assets/earth.png"),
		"venus"   : Planet((50, 50), "assets/earth.png"),
		"earth"   : Planet((50, 50), "assets/earth.png"),
		"mars"    : Planet((50, 50), "assets/earth.png"),
		"jupiter" : Planet((50, 50), "assets/earth.png"),
		"saturn"  : Planet((50, 50), "assets/earth.png"),
		"uranus"  : Planet((50, 50), "assets/earth.png"),
		"neptune" : Planet((50, 50), "assets/earth.png"),
	}


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

	def getChanges(self, forceAll):
		if self.isNewScreen() or forceAll:
			# update everythin
			return self.params
		else:
			# update only things that changed
			changedParams = self.params.copy()
			for key in self.params:
				if self.params[key] == self.oldParams[key]:
					del changedParams[key]
			return changedParams

	# show the changes, increment the param dictionaries
	def frame(self):
		global oldScreen
		self.display.update(self.updateRegions)
		self.updateRegions = []
		self.oldParams = self.params.copy()
		oldScreen = self









'''
Class that draws the home screen
'''
class Home(Screen):
	def __init__(self):
		super(Home, self).__init__()

		# default parameter list
		self.params = OrderedDict([
			("background", False),
		])

		# init the old parameters list
		self.oldParams = self.params.copy()
	
	def frame(self, forceAll=False):
		changedParams = super(Home, self).getChanges(forceAll)

		for key in changedParams:
			rect = self.draw(key, self.params[key])
			self.updateRegions.append(rect);

		super(Home, self).frame()


	# object drawing routines. Returns Rect of area modified
	def draw(self, key, value):
		global assets

		if key == "background":
			if value:
				return pygame.Rect(0,0,0,0)
			else:
				return self.window.fill(pygame.Color(255,255,255))
		else:
			return pygame.Rect(0,0,0,0)

	def click(event):
		pass








'''
Class that draws the play screen
'''
class Play(Screen):
	def __init__(self):
		super(Play, self).__init__()

		# default parameter list
		self.params = OrderedDict([
			("background", False),
			("test", True),
			("mercury", (0.0, 0.0)), # (glow-alpha, glow-alpha-speed)
			("venus",   (0.0, 0.0)),
			("earth",   (0.0, 0.0)),
			("mars",    (0.0, 0.0)),
			("jupiter", (0.0, 0.0)),
			("saturn",  (0.0, 0.0)),
			("uranus",  (0.0, 0.0)),
			("neptune", (0.0, 0.0)),
		])

		# init the old parameters list
		self.oldParams = self.params.copy()
	
	def frame(self, forceAll=False):
		changedParams = super(Play, self).getChanges(forceAll)

		for key in changedParams:
			rect = self.draw(key, self.params[key])
			self.updateRegions.append(rect);

		super(Play, self).frame()


	# object drawing routines. Returns Rect of area modified
	def draw(self, key, value):
		global assets

		if key == "background":
			if value:
				return pygame.Rect(0,0,0,0)
			else:
				return self.window.fill(pygame.Color(255,255,255))
		elif key == "test":
			if value:
				return self.window.blit(assets["test"], (0,0))
			else:
				return pygame.Rect(0,0,0,0)
		elif key == "earth":
			return sprites["earth"].blitSelf(self.window)
		else:
			return pygame.Rect(0,0,0,0)

	def click(event):
		pass
