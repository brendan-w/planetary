
import math
import pygame
from pygame.sprite import Sprite
from pygame.font import Font
from pygame.transform import scale


'''
Base graphics class
'''

class DisplayObject(Sprite):
	def __init__(self, pos, image=None):
		Sprite.__init__(self)
		self.active = True
		self.x = pos[0]
		self.y = pos[1]
		self.image = image
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()

	def blitTo(self, surface):
		if self.active:
			self.rect = surface.blit(self.image, (self.x, self.y))
		else:
			self.rect = pygame.Rect(0,0,0,0)

		return self.rect

	def pointCollide(self, point):
		if self.rect.collidepoint(point) and self.mask != None:
			point = (point[0] - self.x, point[1] - self.y)
			return self.mask.get_at(point)
		else:
			return False

	def setPos(self, p):
		self.x = p.x
		self.y = p.y

	def move(self, p):
		self.x += p.x
		self.y += p.y

	def hash(self):
		return (self.x, self.y, self.active)


'''
Subclasses of DisplayObject
'''


class TiledBackground(DisplayObject):
	def __init__(self, tilePath):
		tile = pygame.image.load(tilePath).convert_alpha()
		tileWidth = tile.get_width()
		tileHeight = tile.get_height()

		screen = pygame.display.get_surface()
		screenWidth = screen.get_width()
		screenHeight = screen.get_height()

		# tile the image
		image = pygame.Surface( (screenWidth, screenHeight) )
		xTiles = int(math.ceil(screenWidth / tileWidth))
		yTiles = int(math.ceil(screenHeight / tileHeight))

		for x in range(xTiles):
			for y in range(yTiles):
				image.blit(tile, (x * tileWidth, y * tileHeight) )		

		super(TiledBackground, self).__init__( (0,0), image)


class Planet(DisplayObject):

	def __init__(self, pos, size, imagePath):
		image = pygame.image.load(imagePath).convert_alpha()
		image = scale(image, size)
		super(Planet, self).__init__(pos, image)

	def setGlow(self):
		pass

class TextBox(DisplayObject):
	def __init__(self, pos, imagePath, fontSize, fontPath):
		self.text = ""
		self.font = Font(fontPath, fontSize)
		image = pygame.image.load(imagePath).convert_alpha()
		super(TextBox, self).__init__(pos, image)

	def hash(self):
		return super(TextBox, self).hash() + (self.text,)
		