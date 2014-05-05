
import pygame
from pygame.sprite import Sprite

class Planet(Sprite):

    def __init__(self, position, image):
       Sprite.__init__(self)

       self.x = position[0]
       self.y = position[1]
       self.image = pygame.image.load(image).convert_alpha()
       self.mask = pygame.mask.from_surface(self.image)
       # self.rect = self.image.get_rect()

    def blitSelf(self, surface):
    	return surface.blit(self.image, (self.x, self.y))
