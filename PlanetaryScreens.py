'''
System for handling STATIC pygame screens efficiently

Screens are handed dictionaries containing the settings for the screen.
The screen class filters this dictionary based on what has changed, and
what needs refreshing.

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
		self.oldParams = {} 

	def filter(self, gameParams):
		global lastScreen

		if lastScreen != self:
			# if the entire screen was changed, update everything
			lastScreen = self
			return gameParams
		else:
			# find out which params changed
			newParams = dict()
			for key in gameParams:
				if self.oldParams.has_key(key):
					if self.oldParams[key] != gameParams[key]:
						newParams[key] = gameParams[key]
				else:
					newParams[key] = gameParams[key]

			self.oldParams = gameParams.copy()
			return newParams

	# default frame drawer, overriden in subclasses
	def frame(self):
		self.display.update(self.updateRegions)
		self.updateRegions = []




'''
Class that draws the home screen
'''
class Home(Screen):
	def __init__(self, display):
		super(Home, self).__init__(display)

	def frame(self, gameParams):
		# figure out which components need updating
		gameParams = super(Home, self).filter(gameParams)

		# update neccessary parts of this screen
		for key in gameParams:
			if key == "background":
				self.window.fill(pygame.Color(255,255,255))
				# self.updateRegions.append(pygame.Rect(0,0,x,y));

		# update the screen
		super(Home, self).frame()



'''
Class that draws the play screen
'''
class Play(Screen):
	def __init__(self, display):
		super(Play, self).__init__(display)

	def frame(self, gameParams):
		# figure out which components need updating
		gameParams = super(Home, self).filter(gameParams)

		# update neccessary parts of this screen
		for key in gameParams:
			pass

		# update the screen
		super(Play, self).frame()
