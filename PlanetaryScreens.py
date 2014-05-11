'''
System for handling STATIC pygame screens efficiently

Each screen object has an OrderedDict of DisplayObjects that can be modified by
the game. When frame() is called on a screen, it filters for changes in each
sprites attributes, and blits the changed graphics. Switching screens forces all
elements to be redrawn.
'''


import pygame
from collections import OrderedDict

from PlanetarySprites import Planet, TiledBackground
from PlanetaryConstants import *

# used for determining screen switches
oldScreen = None



'''
Base class for screens
Handles sprite changes, update regions, and clicks
Subclasses MUST implement draw(key, sprite)
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
				if self.oldSprites.has_key(key):
					if self.sprites[key].hash() == self.oldSprites[key]:
						del changedSprites[key]
			return changedSprites

	def saveOld(self):
		oldScreen = self
		self.oldSprites = self.sprites.copy()
		for key in self.sprites:
			self.oldSprites[key] = self.sprites[key].hash()


	# show the changes, increment the param dictionaries
	def frame(self, forceAll=False):
		global oldScreen

		changedSprites = self.getChanges(forceAll)

		for key in changedSprites:
			rect = self.draw(key, self.sprites[key])
			self.updateRegions.append(rect);

		self.display.update(self.updateRegions)
		self.updateRegions = []
		self.saveOld()

	def pointCollide(self, point):
		response = ""
		for key in self.sprites:
			if self.sprites[key].pointCollide(point):
				response = key
		return response







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
			("background", TiledBackground("assets/space.png")),
			("mercury", Planet(MERCURY_POS, MERCURY_SIZE, "assets/mercury.png")),
			("venus"  , Planet(VENUS_POS,   VENUS_SIZE,   "assets/venus.png")),
			("earth"  , Planet(EARTH_POS,   EARTH_SIZE,   "assets/earth.png")),
			("mars"   , Planet(MARS_POS,    MARS_SIZE,    "assets/mars.png")),
			("jupiter", Planet(JUPITER_POS, JUPITER_SIZE, "assets/jupiter.png")),
			("saturn" , Planet(SATURN_POS,  SATURN_SIZE,  "assets/saturn.png")),
			("uranus" , Planet(URANUS_POS,  URANUS_SIZE,  "assets/uranus.png")),
			("neptune", Planet(NEPTUNE_POS, NEPTUNE_SIZE, "assets/neptune.png")),
		])

		#super(Play, self).saveOld()

	# object drawing routines. Returns Rect of area modified
	def draw(self, key, sprite):
		if isinstance(sprite, Planet):
			return sprite.blitTo(self.window)
		else:
			return sprite.blitTo(self.window)
