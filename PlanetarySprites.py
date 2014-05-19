'''
Sprite object definitions.
DisplayObject is the base class for displaying clickable images.
'''

import math
import pygame
from pygame.sprite import Sprite
from pygame.font import Font
from PlanetaryConstants import *


'''
Base graphics class
'''
class DisplayObject(Sprite):
	def __init__(self, pos, image=None):
		Sprite.__init__(self)
		self.active = True
		self.x = pos[0]
		self.y = pos[1]
		if image != None:
			self.image = image
			self.mask = pygame.mask.from_surface(self.image)
			self.rect = self.image.get_rect()
			self.rect = pygame.Rect(self.x, self.y, self.rect[2], self.rect[3])
		else:
			self.rect = pygame.Rect(self.x, self.y, 0, 0)

	def blitTo(self, surface):
		if self.active:
			self.rect = surface.blit(self.image, (self.x, self.y))
		else:
			self.rect = EMPTY_RECT

		return self.rect

	# collides a global point coordinate with the image mask
	def pointCollide(self, point):
		if self.rect.collidepoint(point) and self.mask != None:
			point = (point[0] - self.x, point[1] - self.y)
			return self.mask.get_at(point)
		else:
			return False
	
	# called every frame
	def animate(self):
		self.rect = pygame.Rect(self.x, self.y, self.rect[2], self.rect[3])

	def setPos(self, p):
		self.x = p.x
		self.y = p.y

	def move(self, p):
		self.x += p.x
		self.y += p.y

	# subclasses should override and append additional values
	def hash(self):
		return (self.x, self.y, self.active)


'''
Subclasses of DisplayObject
'''

# creates a background image by tiling the given image
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

	# blits rectangular portion
	def blitPortion(self, surface, rect):
		return surface.blit(self.image, (rect[0], rect[1]), rect)

	# blits rectangular portion and applies the given mask surface
	def blitMask(self, surface, rect, mask):
		image = mask.copy()
		image.blit(self.image, (0,0), None, pygame.BLEND_RGBA_MULT)
		return surface.blit(image, (rect[0], rect[1]))



# creates a planet with a controlled glow surrounding it
class Planet(DisplayObject):

	def __init__(self, pos, imagePath, glowPath, maskPath):
		image = pygame.image.load(imagePath).convert_alpha()
		self.glow_mask = pygame.image.load(maskPath).convert_alpha()		
		self.glow = pygame.image.load(glowPath).convert_alpha()
		self.glowing = False
		self.glow_alpha = 0
		super(Planet, self).__init__(pos, image)

	def animate(self):
		if self.glowing and self.glow_alpha < 255:
			self.glow_alpha += GLOW_SPEED
		elif not self.glowing and self.glow_alpha > 0:
			self.glow_alpha -= GLOW_SPEED
		self.glow_alpha = clamp(self.glow_alpha, 0, 255)

	def blitTo(self, surface):
		print "planet"
		# can't use set_alpha() because image already contains a per-pixel alpha channel
		if self.glow_alpha != 0:
			glowA = self.glow.copy()
			glowA.fill((255, 255, 255, self.glow_alpha), None, pygame.BLEND_RGBA_MULT)
			surface.blit(glowA, (self.x, self.y))
		return super(Planet, self).blitTo(surface)

	def setGlow(self, glow):
		self.glowing = glow

	def hash(self):
		return super(Planet, self).hash() + (self.glowing, self.glow_alpha)


# renders text
class TextBox(DisplayObject):
	def __init__(self, pos, maxChars, fontPath, fontSize, fontColor):
		self.lines = []
		self.text = ""
		self.text_color = fontColor
		self.max_chars = maxChars
		self.font = Font(fontPath, fontSize)

		self.setText("Question gets displayed here.")
		super(TextBox, self).__init__(pos)

	def animate(self):
		pass

	def blitTo(self, surface):
		print "textbox"

		# loop through the lines and render
		rects = []
		for index, line in enumerate(self.lines):
			text_image = self.font.render(line, True, self.text_color)
			position = (self.x, self.y + (index * text_image.get_height()))
			self.rect = surface.blit(text_image, position)

		if len(rects) > 0:
			self.rect = EMPTY_RECT.unionall(rects)
		else:
			self.rect = EMPTY_RECT
		return self.rect

	def setText(self, text):
		text = text.strip()
		self.text = text

		# split the text into multiple lines across spaces
		self.lines = []
		while len(text) > self.max_chars:
			line = text[0:self.max_chars]
			space = line.rfind(" ")
			if space != -1:
				self.lines.append(line[0:space])
				text = text[space:].strip()
			else:
				self.lines.append(line)
				text = text[max_chars:].strip()

		self.lines.append(text) #dont forget about the last line!

	def hash(self):
		return super(TextBox, self).hash() + (self.text, self.text_color, self.max_chars)
		