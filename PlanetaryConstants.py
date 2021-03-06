
from random import randint
from pygame import Rect
from pygame import Color


'''
Constants
'''

EMPTY_RECT = Rect(0,0,0,0)



# Object IDs
BACKGROUND = "background"
LOGO = "logo"
TEXTBOX = "textbox"
OK_BUTTON = "ok"
HOME_BUTTON = "home"
PLAY_BUTTON = "play"

MERCURY = "mercury"
VENUS =   "venus"
EARTH =   "earth"
MARS =    "mars"
JUPITER = "jupiter"
SATURN =  "saturn"
URANUS =  "uranus"
NEPTUNE = "neptune"

PLANETS = [MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE]



# Layout
V = 100
MERCURY_POS = (0,   510 + V)
VENUS_POS =   (70,  480 + V)
EARTH_POS =   (170, 450 + V)
MARS_POS =    (280, 430 + V)
JUPITER_POS = (360, 230 + V)
SATURN_POS =  (610, 110 + V)
URANUS_POS =  (880, 90 + V)
NEPTUNE_POS = (1020,0 + V)

TEXTBOX_POS = (15,0)

OK_BUTTON_POS = (15, 130)
HOME_BUTTON_POS = (935, 700)
PLAY_BUTTON_POS = (475, 500)

LOGO_POS = (400, 50)

# Colors
GLOW_WHITE = (255, 255, 255)
GLOW_RED =   (255, 50, 50)
GLOW_GREEN = (0, 255, 0)
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 136, 255)


# Text
MAX_CHARS = 50
FONT_SIZE = 40

WIN_TEXT = "Correct!"
LOSE_TEXT = "Incorrect"
NEXT_FACT_TEXT = "Next planet fact"


# Animation
GLOW_FADE_FRAMES = 6

FADE_SPEED = 10





'''
Utilities
'''

def clamp(value, min_value, max_value):
	return max(min(value, max_value), min_value)

def mapValue(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min