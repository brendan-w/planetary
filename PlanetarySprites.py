
import pygame
from pygame.sprite import Sprite


class DisplayObject(Sprite):
	def __init__(self, pos, image):
		Sprite.__init__(self)
		self.x = pos[0]
		self.y = pos[1]
		self.image = pygame.image.load(image).convert_alpha()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()

	def blitTo(self, surface):
		return surface.blit(self.image, (self.x, self.y))

	def clickMask(self, point):
		return self.mask.get_at(point)

	def setPos(self, p):
		self.x = p.x
		self.y = p.y

	def move(self, p):
		self.x += p.x
		self.y += p.y

	def getCompare(self):
		return (self.x, self.y)


class Planet(DisplayObject):

	def __init__(self, pos, image):
		super(Planet, self).__init__(pos, image)

	def setGlow(self):
		pass
