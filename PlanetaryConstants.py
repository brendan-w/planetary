
'''
Planet layout information
'''

MERCURY = "mercury"
VENUS =   "venus"
EARTH =   "earth"
MARS =    "mars"
JUPITER = "jupiter"
SATURN =  "saturn"
URANUS =  "uranus"
NEPTUNE = "neptune"




QUESTION_POS = (0,0)
QUESTION_FONT_SIZE = 20

GLOW_SPEED = 0.05


MERCURY_SIZE = 30
VENUS_SIZE =   60
EARTH_SIZE =   70
MARS_SIZE =    50
JUPITER_SIZE = 250
SATURN_SIZE =  350
URANUS_SIZE =  120
NEPTUNE_SIZE = 110


MERCURY_POS = (0,   450 - (MERCURY_SIZE / 2))
VENUS_POS =   (60,  450 - (VENUS_SIZE   / 2))
EARTH_POS =   (150, 450 - (EARTH_SIZE   / 2))
MARS_POS =    (240, 450 - (MARS_SIZE    / 2))
JUPITER_POS = (320, 450 - (JUPITER_SIZE / 2))
SATURN_POS =  (590, 450 - (SATURN_SIZE  / 2))
URANUS_POS =  (880, 450 - (URANUS_SIZE  / 2))
NEPTUNE_POS = (1030,450 - (NEPTUNE_SIZE / 2))


def clamp(value, min_value, max_value):
	return max(min(value, max_value), min_value)
