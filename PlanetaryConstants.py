
from random import randint
from pygame import Rect
from pygame import Color


'''
Constants
'''

EMPTY_RECT = Rect(0,0,0,0)


# Game Logic
TOTAL_STATES = 6

RESULT_WAIT = 100
CORRECT_WAIT = 100


# Object IDs
BACKGROUND = "background"
QUESTION = "question"
FACT = "fact"
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
QUESTION_POS = (15,0)
FACT_POS =     (15,150)



# Colors
GLOW_WHITE = (255, 255, 255)
GLOW_RED =   (255, 50, 50)
GLOW_GREEN = (0, 255, 0)
FONT_COLOR = Color(255,255,255,255)


# Text
FONT = "assets/titillium-regular.ttf"
QUESTION_MAX_CHARS = 40
QUESTION_FONT_SIZE = 40
FACT_MAX_CHARS = 40
FACT_FONT_SIZE = 40


# Animation
GLOW_SPEED_NORMAL = 50 #0-255, per frame





'''
Utilities
'''

def clamp(value, min_value, max_value):
	return max(min(value, max_value), min_value)

def randomColor():
	return (randint(0, 255), randint(0, 255), randint(0, 255))