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
	def __init__(self, pos, clickable, image=None):
		Sprite.__init__(self)
		self.active = True
		self.x = pos[0]
		self.y = pos[1]
		self.mask = None
		if image != None:
			self.image = image
			self.rect = self.image.get_rect()
			self.rect = pygame.Rect(self.x, self.y, self.rect[2], self.rect[3])

			if clickable:
				self.mask = pygame.mask.from_surface(self.image)
		else:
			self.rect = pygame.Rect(self.x, self.y, 0, 0)

	def blitTo(self, surface):
		if self.active:
			self.rect = surface.blit(self.image, (self.x, self.y))
		return self.rect

	# collides a global point coordinate with the image mask
	def pointCollide(self, point):
		if self.active and self.mask != None and self.rect.collidepoint(point):
			point = (point[0] - self.x, point[1] - self.y)
			return self.mask.get_at(point)
		else:
			return False
	
	# sets the opacity of the given image
	def setOpacity(self, image, opacity, color=(255,255,255)):
		imageCopy = image.copy()
		rgba = color + (opacity,)
		imageCopy.fill(rgba, None, pygame.BLEND_RGBA_MULT)
		return imageCopy

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

class Image(DisplayObject):
	def __init__(self, pos, imagePath):
		image = pygame.image.load(imagePath).convert_alpha()
		super(Image, self).__init__(pos, False, image)


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

		super(TiledBackground, self).__init__( (0,0), False, image)

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
		glow = pygame.image.load(glowPath).convert_alpha()
		self.glow_white = []
		self.glow_green = []
		self.glow_red = []

						  # +1 for final 100% frame
		for i in range(0, GLOW_FADE_FRAMES + 1):
			i += 1
			opacity = mapValue(i, 0, GLOW_FADE_FRAMES + 1, 0, 255)
			self.glow_white.append(self.setOpacity(glow, opacity, GLOW_WHITE))
			self.glow_green.append(self.setOpacity(glow, opacity, GLOW_GREEN))
			self.glow_red.append(self.setOpacity(glow, opacity, GLOW_RED))


		self.glowing = False
		self.glow_frame = 0
		self.glow_color = GLOW_WHITE
		self.pulsing = False
		super(Planet, self).__init__(pos, True, image)

	def animate(self):
		# pulser
		if self.pulsing:
			if self.glow_frame <= 0:
				self.setGlow(True)
			elif self.glow_frame >= GLOW_FADE_FRAMES:
				self.setGlow(False)

		# opacity fader
		if self.glowing and self.glow_frame < GLOW_FADE_FRAMES:
			self.glow_frame += 1
		elif not self.glowing and self.glow_frame > 0:
			self.glow_frame -= 1
		self.glow_frame = clamp(self.glow_frame, 0, GLOW_FADE_FRAMES)

	def blitTo(self, surface):
		# can't use set_alpha() because image already contains a per-pixel alpha channel
		if self.glow_frame != 0:
			glow = None
			if self.glow_color == GLOW_WHITE:
				glow = self.glow_white[self.glow_frame]
			elif self.glow_color == GLOW_GREEN:
				glow = self.glow_green[self.glow_frame]
			elif self.glow_color == GLOW_RED:
				glow = self.glow_red[self.glow_frame]

			if glow != None:
				surface.blit(glow, (self.x, self.y))

		return super(Planet, self).blitTo(surface)

	def setGlow(self, glow):
		self.glowing = glow

	def setGlowColor(self, color):
		self.glow_color = color

	def startPulsing(self):
		self.pulsing = True

	def stopPulsing(self):
		self.pulsing = False
		self.setGlow(False)

	def hash(self):
		return super(Planet, self).hash() + (self.glowing, self.glow_color, self.glow_frame)


# renders text
class TextBox(DisplayObject):
	def __init__(self, pos, maxChars, font):
		self.lines = []
		self.text = ""
		self.text_color = FONT_COLOR
		self.max_chars = maxChars
		self.font = font
		self.alpha = 0
		self.alpha_speed = FADE_SPEED

		self.setText("TextBox")
		super(TextBox, self).__init__(pos, False)
		self.active = False

	def animate(self):
		# opacity fader
		if self.active and self.alpha < 255:
			self.alpha += self.alpha_speed
		elif not self.active and self.alpha > 0:
			self.alpha -= self.alpha_speed
		self.alpha = clamp(self.alpha, 0, 255)

	def blitTo(self, surface):

		# loop through the lines and render
		rects = []
		for index, line in enumerate(self.lines):
			self.image = self.font.render(line, True, self.text_color)
			self.image = self.setOpacity(self.image, self.alpha)
			position = (self.x, self.y + (index * self.image.get_height()))
			rects.append(surface.blit(self.image, position))

		rects.append(self.rect) # causes textbox rect to expand to largest text so far
		self.rect = EMPTY_RECT.unionall(rects)
		
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
		return super(TextBox, self).hash() + (self.text, self.text_color, self.max_chars, self.alpha)




class Button(DisplayObject):
	def __init__(self, pos, imagePath, font, text):
		image = pygame.image.load(imagePath).convert_alpha()
		image = self.setOpacity(image, 255, BUTTON_COLOR)
		textGraphics = font.render(text, True, (255, 255, 255))

		xoff = int((image.get_width() - textGraphics.get_width()) / 2)
		yoff = int((image.get_height() - textGraphics.get_height()) / 2)
		image.blit(textGraphics, (xoff, yoff))

		self.alpha = 0
		self.alpha_speed = FADE_SPEED

		super(Button, self).__init__(pos, True, image)

		self.active = False

	def animate(self):
		# opacity fader
		if self.active and self.alpha < 255:
			self.alpha += self.alpha_speed
		elif not self.active and self.alpha > 0:
			self.alpha -= self.alpha_speed
		self.alpha = clamp(self.alpha, 0, 255)

	def blitTo(self, surface):
		image = self.setOpacity(self.image, self.alpha)
		return surface.blit(image, (self.x, self.y))

	def hash(self):
		return super(Button, self).hash() + (self.alpha,)
