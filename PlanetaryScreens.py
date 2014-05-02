

import pygame


'''
Base class for screens
'''
class Screen(object):

	def __init__(self, display):
		self.display = display
		self.window = display.get_surface()
		self.updateRegions = []

	def update(self, drawAll):
		if drawAll:
			self.display.update()
		else:
			self.display.update(self.updateRegions)
		
		self.updateRegions = []



'''
Class that draws the home screen
'''
class Home(Screen):
	def __init__(self, display):
		super(Home, self).__init__(display)

	def frame(self, gameParams, drawAll=False):
		# update neccessary parts of this screen
		self.window.fill(pygame.Color(255,255,255))
		# update the screen
		super(Home, self).update(drawAll)


'''
Class that draws the play screen
'''
class Play(Screen):
	def __init__(self, display):
		super(Play, self).__init__(display)

	def frame(self, gameParams, drawAll=False):
		# update neccessary parts of this screen

		# update the screen
		super(Play, self).update(drawAll)
