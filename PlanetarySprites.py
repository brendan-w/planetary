
import pygame
from pygame.sprite import Sprite


'''
Base graphics class
'''

class DisplayObject(Sprite):
	def __init__(self, pos, image):
		Sprite.__init__(self)
		self.active = True
		self.x = pos[0]
		self.y = pos[1]
		self.image = pygame.image.load(image).convert_alpha()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()

	def blitTo(self, surface):
		if self.active:
			self.rect = surface.blit(self.image, (self.x, self.y))
		else:
			self.rect = pygame.Rect(0,0,0,0)

		return self.rect

	def pointCollide(self, point):
		if self.rect.collidepoint(point):
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
		return (self.x, self.y)


'''
Subclasses of DisplayObject
'''


class Planet(DisplayObject):

	def __init__(self, pos, image):
		super(Planet, self).__init__(pos, image)

	def setGlow(self):
		pass
