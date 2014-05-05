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

def load():
	global assets

	assets = {
		"test" : pygame.image.load("assets/python_test_600x600.png").convert_alpha()
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
		self.sprites = OrderedDict()
		self.oldSprites = OrderedDict()

	def isNewScreen(self):
		global oldScreen
		return (oldScreen != self)

	def getChanges(self, forceAll):
		if self.isNewScreen() or forceAll:
			# update everything
			return self.sprites
		else:
			# update only things that changed
			changedSprites = self.sprites.copy()
			for key in self.sprites:
				if self.sprites[key].getCompare() == self.oldSprites[key]:
					del changedSprites[key]
			return changedSprites

	def saveOld(self):
		self.oldSprites = self.sprites.copy()
		for key in self.sprites:
			self.oldSprites[key] = self.sprites[key].getCompare()


	# show the changes, increment the param dictionaries
	def frame(self):
		global oldScreen
		self.display.update(self.updateRegions)
		self.updateRegions = []
		self.saveOld()
		oldScreen = self









'''
Class that draws the home screen
'''
class Home(Screen):
	def __init__(self):
		super(Home, self).__init__()








'''
Class that draws the play screen
'''
class Play(Screen):
	def __init__(self):
		super(Play, self).__init__()

		self.sprites = OrderedDict([
			("mercury", Planet((50, 50), "assets/earth.png")),
			("venus"  , Planet((50, 50), "assets/earth.png")),
			("earth"  , Planet((50, 50), "assets/earth.png")),
			("mars"   , Planet((50, 50), "assets/earth.png")),
			("jupiter", Planet((50, 50), "assets/earth.png")),
			("saturn" , Planet((50, 50), "assets/earth.png")),
			("uranus" , Planet((50, 50), "assets/earth.png")),
			("neptune", Planet((50, 50), "assets/earth.png")),
		])

		super(Play, self).saveOld()
	
	def frame(self, forceAll=False):
		changedSprites = super(Play, self).getChanges(forceAll)

		for key in changedSprites:
			rect = self.draw(key, self.sprites[key])
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
			return self.sprites["earth"].blitTo(self.window)
		else:
			return pygame.Rect(0,0,0,0)

	def click(self, event, point):
		for param in self.sprites:
			if sprites.has_key(param):
				pass
