'''
System for handling STATIC pygame screens efficiently

Each screen object has an OrderedDict of DisplayObjects that can be modified by
the game. When frame() is called on a screen, it filters for changes in each
sprites attributes, and blits the changed graphics. Switching screens forces all
elements to be redrawn.

all sprites should be a (or be derived from) DisplayObject (see PlanetarySprites.py)
'''


import pygame
from collections import OrderedDict

from PlanetarySprites import *
from PlanetaryConstants import *

# used for determining screen switches
oldScreen = None



'''
Base class for screens
Handles sprite changes, update regions, and clicks
Subclasses must implement draw(key, sprite)
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
		global oldScreen
		oldScreen = self
		self.oldSprites = self.sprites.copy()
		for key in self.sprites:
			self.oldSprites[key] = self.sprites[key].hash()


	# show the changes, increment the param dictionaries
	def frame(self, forceAll=False):

		for key in self.sprites:
			self.sprites[key].animate()

		changedSprites = self.getChanges(forceAll)

		for key in changedSprites:
			rect = self.draw(key, self.sprites[key])
			self.updateRegions.append(rect);

		self.display.update(self.updateRegions)
		self.updateRegions = []
		self.saveOld()

	# returns the key of the topmost sprite that collides with the point
	def click(self, point):
		response = None
		for key in self.sprites:
			if self.sprites[key].pointCollide(point):
				response = key
		return response

	#default handler
	def draw(self, key, sprite):
		return sprite.blitTo(self.window)

	#default handler
	def mousemove(self, point):
		pass




'''
Class that draws the home screen
'''
class Home(Screen):
	def __init__(self):
		super(Home, self).__init__()

		self.sprites = OrderedDict([
			(BACKGROUND, TiledBackground("assets/space.png")),
		])

	def draw(self, key, sprite):
		return sprite.blitTo(self.window)




'''
Class that draws the play screen
'''
class Play(Screen):
	def __init__(self):
		super(Play, self).__init__()

		self.sprites = OrderedDict([
			(BACKGROUND, TiledBackground("assets/space.png")),
			(QUESTION,   TextBox(QUESTION_POS, QUESTION_MAX_CHARS, FONT, QUESTION_FONT_SIZE)),
			(FACT,     TextBox(FACT_POS, FACT_MAX_CHARS, FONT, FACT_FONT_SIZE)),
			(MERCURY, Planet(MERCURY_POS, "assets/mercury.png", "assets/mercury_glow.png", "assets/mercury_mask.png")),
			(VENUS,   Planet(VENUS_POS,   "assets/venus.png",   "assets/venus_glow.png",   "assets/venus_mask.png")),
			(EARTH,   Planet(EARTH_POS,   "assets/earth.png",   "assets/earth_glow.png",   "assets/earth_mask.png")),
			(MARS,    Planet(MARS_POS,    "assets/mars.png",    "assets/mars_glow.png",    "assets/mars_mask.png")),
			(JUPITER, Planet(JUPITER_POS, "assets/jupiter.png", "assets/jupiter_glow.png", "assets/jupiter_mask.png")),
			(SATURN,  Planet(SATURN_POS,  "assets/saturn.png",  "assets/saturn_glow.png",  "assets/saturn_mask.png")),
			(URANUS,  Planet(URANUS_POS,  "assets/uranus.png",  "assets/uranus_glow.png",  "assets/uranus_mask.png")),
			(NEPTUNE, Planet(NEPTUNE_POS, "assets/neptune.png", "assets/neptune_glow.png", "assets/neptune_mask.png")),
		])

		# custom screen variables
		self.mouseOverEnabled = True

		#super(Play, self).saveOld()


	# object drawing routines. Returns Rect of area modified
	def draw(self, key, sprite):
		if isinstance(sprite, Planet):
			# blit the masked portion of the background
			self.sprites[BACKGROUND].blitMask(self.window, sprite.rect, sprite.glow_mask)
			return sprite.blitTo(self.window)

		elif isinstance(sprite, TextBox):
			# blit the portion of the background
			self.sprites[BACKGROUND].blitPortion(self.window, sprite.rect)
			return sprite.blitTo(self.window)

		else:
			return sprite.blitTo(self.window)

	def mousemove(self, point):
		if self.mouseOverEnabled:
			for key in self.sprites:
				sprite = self.sprites[key]
				if isinstance(sprite, Planet):
					if sprite.pointCollide(point):
						sprite.setGlow(True)
					else:
						sprite.setGlow(False)


	# custom, screen-specific functions

	def hideQuestion(self):
		self.sprites[QUESTION].active = False

	def setQuestion(self, question):
		sprite = self.sprites[QUESTION]
		sprite.active = True
		sprite.setText(question)

	def hideFact(self):
		self.sprites[FACT].active = False

	def setFact(self, fact):
		sprite = self.sprites[FACT]
		sprite.active = True
		sprite.setText(fact)

	def startPulse(self, answer):
		sprite = self.sprites[answer[1]]
		if answer[0]:
			sprite.setGlowColor(GLOW_GREEN)
		else:
			sprite.setGlowColor(GLOW_RED)
		sprite.startPulsing()

	def stopPulse(self, answer):
		sprite = self.sprites[answer[1]]
		sprite.setGlowColor(GLOW_WHITE)
		sprite.stopPulsing()
