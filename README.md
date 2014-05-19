Planetary
=========

Solar system game for the XO PC. Teaches kids about the arrangment of the solar system, and about the planets themselves.


File Explanations
=================


###PlanetaryActivity.py (Entry point)

Handles basic sugar activity things, like the toolbar and read_file/write_file


###Planetary.py (Pygame App)

Handles primary game logic and UI. Manages the game state and data. Switches and interacts with screen objects


###PlanetaryScreens.py (Pygame App)

Defines classes for the various screens in the game ("Home" and "Play" in this case). Each screen class manages its own sprites, and computes the changes from one frame to the next.


###PlanetarySprites.py (Pygame App)

Defines individual sprites (ie. "Planet", "Background", "TextBox"). Sprites handle their own graphics internally, and contain functions and switches for the screen class to change.


###PlanetaryConstants.py (Pygame App)

Game-wide constants and utility functions.


###init_data.json (question set / game state)

Written in JSON, questions are stored in one of two lists. "live" holds questions that are in play (that the user should be able to answer), and "wait" holds potential questions. Each question can have multiple answers. This file is only used for starting a game. Once a game is started and saved, the instance JSON (game state) is saved to the journal.
