'''
Constants
'''

BACKGROUND = "background"
MERCURY = "mercury"
VENUS =   "venus"
EARTH =   "earth"
MARS =    "mars"
JUPITER = "jupiter"
SATURN =  "saturn"
URANUS =  "uranus"
NEPTUNE = "neptune"

V = 100
MERCURY_POS = (0,   510 + V)
VENUS_POS =   (70,  480 + V)
EARTH_POS =   (170, 450 + V)
MARS_POS =    (280, 430 + V)
JUPITER_POS = (360, 230 + V)
SATURN_POS =  (610, 110 + V)
URANUS_POS =  (880, 90 + V)
NEPTUNE_POS = (1020,0 + V)

GLOW_SPEED = 50 #0-255, per frame

QUESTION_POS = (0,0)
QUESTION_MAX_CHARS = 40
QUESTION_FONT_SIZE = 50


'''
Utilities
'''

def clamp(value, min_value, max_value):
	return max(min(value, max_value), min_value)
