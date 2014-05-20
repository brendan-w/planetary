Planetary
=========

Solar system game for the XO PC. Teaches kids about the arrangment of the solar system, and about the planets themselves.

###Requirements
>Python 2.7
>Pygame

How to Run
=========
There are multiple ways to play Planetary. The game can be played as a standalone pygame app, or as an activity on an XO.


###Running as Pygame App
This game can be played as a desktop application. As long as python and pygame are installed, simply run Planetary.py to play and test. Please note, this method does NOT use any XO or sugargame components.


###Running on an XO
Get a flash drive (or USB volume of your choice), copy the Planetary-#.xo file into the root. Then, plug the drive into XO, and go to the journal. After a second or two, a small flash drive icon will appear in the lower left corner. Click this icon, and you will be presented with a file list. Simply click on the Planetary-#.xo file, and it will install and run.


File Explanations
=================


###PlanetaryActivity.py (Entry point)
Wrapper to run pygame as an Activity on an XO. Handles basic sugar activity things, like the toolbar and read_file/write_file


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
